nextflow.enable.dsl=2

process PREPARE {
 label 'prepare'
 publishDir "${params.outdir}/metadata", mode:'copy'
 input:
 path 'matrix.csv'
 path 'run-grid.json'
 path 'recipe.json'
 path source_manifest
 path script
 path scoring
 path intake
 path science_module
 path representations
 output:
 path 'pixels.npy', emit: pixels
 path 'object_ids.csv', emit: ids
 path 'manifest.json', emit: manifest
 script:
 """
 python research.py prepare --input matrix.csv --grid run-grid.json --recipe recipe.json --source-manifest source_manifest.json --image '${params.image ?: "local"}'
 """
 stub:
 """
 python research.py prepare --input matrix.csv --grid run-grid.json --recipe recipe.json --source-manifest source_manifest.json --image '${params.image ?: "local"}' 
 """
}
process UMAP_CHUNK {
 tag "${cid}:${lo}-${hi}"
 label 'umap'
 publishDir { "${params.outdir}/configs/${cid}/representation" }, mode:'copy', pattern:'*.representation.*'
 input:
 tuple val(cid), val(lo), val(hi)
 path pixels
 path manifest
 path 'run-grid.json'
 path 'recipe.json'
 path script
 path scoring
 path intake
 path science_module
 path representations
 output:
 tuple val(cid), path("${cid}.seeds-*.npz")
 path "*.representation.*", optional:true, emit: representation
 script:
 """
 python research.py seeds --pixels pixels.npy --manifest manifest.json --grid run-grid.json --recipe recipe.json --config '${cid}' --start ${lo} --end ${hi}
 """
 stub:
 """
 touch '${cid}.seeds-${lo}-${hi}.npz'
 """
}
process CONCAT {
 tag cid
 label 'concat'
 publishDir { "${params.outdir}/configs/${cid}/embeddings" }, mode:'copy', pattern:'*.embedding.npy'
 input:
 tuple val(cid), path(chunks)
 path manifest
 path script
 path scoring
 path intake
 path science_module
 path representations
 output:
 tuple val(cid), path("${cid}.embedding.npy"), path("${cid}.distances.npy"), path("${cid}.ensemble.json")
 script:
 """
 python research.py concat --config '${cid}' --manifest manifest.json
 """
 stub:
 """
 touch '${cid}.embedding.npy' '${cid}.distances.npy' '${cid}.ensemble.json'
 """
}
process GRID {
 publishDir { "${params.outdir}/configs/${cid}/grid" }, mode:'copy'
 tag "${cid}:min_samples=${ms}"
 label 'grid'
 input:
 tuple val(cid), path(embedding), path(distances), path(ensemble), val(ms)
 path manifest
 path script
 path scoring
 path intake
 path science_module
 path representations
 output:
 path '*.metrics.csv', emit: metrics
 path '*.labels.npz', emit: labels
 script:
 """
 python research.py grid --config '${cid}' --embedding '${embedding}' --distances '${distances}' --ensemble '${ensemble}' --min-samples ${ms} --manifest manifest.json
 """
 stub:
 """
 touch '${cid}.ms${ms}.metrics.csv' '${cid}.ms${ms}.labels.npz'
 """
}
process RANK {
 label 'rank'
 publishDir "${params.outdir}/results", mode:'copy'
 input:
 path metrics
 path candidate_labels
 path ids
 path manifest
 path 'run-grid.json'
 path 'recipe.json'
 path script
 path scoring
 path intake
 path science_module
 path representations
 output:
 path '*.csv'
 path 'scoring.json'
 path 'run_manifest.json'
 script:
 """
 python research.py rank --grid run-grid.json --recipe recipe.json --ids object_ids.csv --manifest manifest.json
 """
 stub:
 """
 printf '%s\\n' '{"status":"STUB_WIRING_ONLY"}' > run_manifest.json
 touch pooled_global_ranked.csv scoring.json
 """
}
workflow {
 if (!params.input || !params.grid || !params.outdir) error 'Supply --input, --grid and --outdir'
 if (!(params.seed_chunk.toString() ==~ /[1-9][0-9]{0,3}/) || (params.seed_chunk as int)>1000) error 'seed_chunk must be an integer 1..1000'
 if (!(params.prepare_only.toString() in ['true','false'])) error 'prepare_only must be true or false'
 if (params.image && !(params.image ==~ /[a-zA-Z0-9][a-zA-Z0-9._:\/-]*@sha256:[0-9a-f]{64}/)) error 'Image must be an immutable repository digest'
 if (workflow.profile.tokenize(',').contains('awsbatch') && workflow.profile.tokenize(',').contains('gcp'))
   error 'Choose exactly one cloud execution profile per run'
 if (workflow.profile.tokenize(',').contains('gcp')) {
   if (!params.image || !params.google_project || !params.google_location || !params.google_service_account)
     error 'Use the generated Google Batch params file'
   if (workflow.stubRun) error 'Use the local profile for stub checks'
   if (!params.input.startsWith('gs://') || !params.outdir.startsWith('gs://'))
     error 'Google Batch requires explicit GCS input and output paths'
 }
 if (workflow.profile.tokenize(',').contains('awsbatch')) {
   if (!params.image || !params.queue || !params.region || !params.job_role || !params.execution_role || !params.log_group)
     error 'Use the generated AWS Batch params file'
   if (workflow.stubRun) error 'Use the local profile for stub checks'
   if (!params.input.startsWith('s3://') || !params.outdir.startsWith('s3://'))
     error 'AWS Batch requires explicit S3 input and output paths'
 }
 def gf=file(params.grid,checkIfExists:true)
 def recipe=file("${projectDir}/conf/recipe.json",checkIfExists:true)
 def source=file("${projectDir}/source_manifest.json",checkIfExists:true)
 def script=file("${projectDir}/bin/research.py",checkIfExists:true)
 def scoring=file("${projectDir}/bin/freeze5_scoring.py",checkIfExists:true)
 def intake=file("${projectDir}/bin/matrix_intake.py",checkIfExists:true)
 def science_module=file("${projectDir}/bin/science_config.py",checkIfExists:true)
 def representations=file("${projectDir}/bin/dimple_representations",checkIfExists:true)
 PREPARE(file(params.input,checkIfExists:true),gf,recipe,source,script,scoring,intake,science_module,representations)
 if (params.prepare_only.toString() == 'false') {
   def settings=PREPARE.out.manifest.map { manifest -> new groovy.json.JsonSlurper().parseText(manifest.text).resolved_science }
   def tasks=settings.flatMap { cfg ->
     cfg.configs.collectMany { c ->
       def repeats=cfg.seeds[c.config_id].size()
       (1..repeats).step(params.seed_chunk as int).collect { lo -> tuple(c.config_id,lo,Math.min(repeats,lo+(params.seed_chunk as int)-1)) }
     }
   }
   UMAP_CHUNK(tasks,PREPARE.out.pixels,PREPARE.out.manifest,gf,recipe,script,scoring,intake,science_module,representations)
   CONCAT(UMAP_CHUNK.out[0].groupTuple().map { cid, chunks -> tuple(cid, chunks.sort { a,b -> a.name <=> b.name }) },PREPARE.out.manifest,script,scoring,intake,science_module,representations)
   def grids=CONCAT.out.combine(settings).flatMap { cid,embedding,distances,ensemble,cfg -> cfg.hdbscan.min_samples.collect { ms -> tuple(cid,embedding,distances,ensemble,ms) } }
   GRID(grids,PREPARE.out.manifest,script,scoring,intake,science_module,representations)
   RANK(GRID.out.metrics.collect().map { paths -> paths.sort { a,b -> a.name <=> b.name } },GRID.out.labels.collect().map { paths -> paths.sort { a,b -> a.name <=> b.name } },PREPARE.out.ids,PREPARE.out.manifest,gf,recipe,script,scoring,intake,science_module,representations)
 }
}
