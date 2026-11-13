"""Strict portable science settings; baseline recipe remains immutable."""
import copy
import itertools
import json
import math
import re
from dimple_representations.config import _base_config, as_list, UMAP_KEYS, SUPPORTED_UMAP_METRICS, SUPPORTED_HDBSCAN_METRICS

ALIASES = {'grid_eps':'cluster_selection_epsilon', 'grid_min_samples':'min_samples', 'grid_min_cluster_size':'min_cluster_size'}
GRID_KEYS = set(ALIASES.values())

def keys(value, allowed, name):
    if not isinstance(value, dict) or set(value)-set(allowed):
        raise ValueError('Unknown or invalid '+name+' settings')

def integer(value, minimum, name):
    if isinstance(value,bool) or not isinstance(value,int) or value<minimum:
        raise ValueError(name+' must be an integer >= '+str(minimum))

def parameter_values(value, cast=None):
    if isinstance(value,dict):
        keys(value,{'start','stop','step'},'parameter range')
    raw=list(value.values()) if isinstance(value,dict) else value if isinstance(value,list) else [value]
    if cast in (int,float):
        if any(isinstance(v,bool) for v in raw): raise ValueError('Numeric parameter cannot be Boolean')
        if cast is int and any(isinstance(v,float) and not v.is_integer() for v in raw): raise ValueError('Integer parameter cannot be fractional')
    return as_list(value,cast)

def resolved_science(grid):
    custom=grid.get('science',{})
    keys(custom, {'backend','umap','execution','hdbscan','pca','ica',*ALIASES}, 'science')
    defaults=_base_config(); backend=custom.get('backend','umap')
    if backend not in ('umap','pca','ica'): raise ValueError('backend must be umap, pca or ica')
    execution={k:defaults['execution'][k] for k in ('n_random_states','legacy_ensemble_seeds')}
    keys(custom.get('execution',{}),execution,'execution'); execution.update(custom.get('execution',{}))
    integer(execution['n_random_states'],1,'n_random_states')
    if type(execution['legacy_ensemble_seeds']) is not bool: raise ValueError('legacy_ensemble_seeds must be Boolean')
    hdb=custom.get('hdbscan',{})
    extra_keys={'metric','alpha','cluster_selection_method','cluster_selection_persistence','allow_single_cluster','max_cluster_size'}
    keys(hdb, GRID_KEYS|extra_keys|{'grid'},'hdbscan')
    if 'grid' in hdb:
        keys(hdb['grid'],GRID_KEYS|extra_keys,'hdbscan.grid')
        if (set(hdb)-{'grid'}) & set(hdb['grid']): raise ValueError('Duplicate HDBSCAN grid fields')
        hdb={**{k:v for k,v in hdb.items() if k!='grid'},**hdb['grid']}
    hdb_parameters={k:hdb.get(k,defaults['hdbscan'][k]) for k in extra_keys}
    hdb={k:v for k,v in hdb.items() if k not in extra_keys}
    hdb_parameters={k:parameter_values(v,float if k in ('alpha','cluster_selection_persistence') else int if k=='max_cluster_size' else None) for k,v in hdb_parameters.items()}
    for key,values in hdb_parameters.items():
        if not values or len({json.dumps(v,sort_keys=True) for v in values})!=len(values): raise ValueError('Empty or duplicate HDBSCAN '+key)
    if any(v not in SUPPORTED_HDBSCAN_METRICS for v in hdb_parameters['metric']): raise ValueError('Invalid HDBSCAN metric')
    if any(v not in ('eom','leaf') for v in hdb_parameters['cluster_selection_method']): raise ValueError('Invalid HDBSCAN method')
    if any(type(v) is not bool for v in hdb_parameters['allow_single_cluster']): raise ValueError('allow_single_cluster must be Boolean')
    for v in hdb_parameters['max_cluster_size']: integer(v,0,'max_cluster_size')
    for key in ('alpha','cluster_selection_persistence'):
        for value in hdb_parameters[key]:
            if isinstance(value,bool) or not isinstance(value,(int,float)) or not math.isfinite(value) or value<0 or (key=='alpha' and value==0): raise ValueError('Invalid HDBSCAN '+key)
    if 'grid' in hdb:
        keys(hdb['grid'],GRID_KEYS,'hdbscan.grid')
        if set(hdb)-{'grid'}: raise ValueError('Use hdbscan.grid or direct grid fields, not both')
        hdb=hdb['grid']
    hdb=copy.deepcopy(hdb)
    for alias,key in ALIASES.items():
        if alias in custom:
            if key in hdb: raise ValueError('Duplicate HDBSCAN grid definition')
            hdb[key]=custom[alias]
    hdb={k:parameter_values(hdb.get(k,defaults['hdbscan'][k]),float if k=='cluster_selection_epsilon' else int) for k in GRID_KEYS}
    for key,values in hdb.items():
        if key!='cluster_selection_epsilon':
            for value in values: integer(value,2 if key=='min_cluster_size' else 1,key)
        if not values or len(set(values))!=len(values): raise ValueError('Grid values must be nonempty and unique')
        if any(not math.isfinite(v) or v < (0 if key=='cluster_selection_epsilon' else 2 if key=='min_cluster_size' else 1) for v in values): raise ValueError('Invalid HDBSCAN grid value')
    if any(v and v<max(hdb['min_cluster_size']) for v in hdb_parameters['max_cluster_size']): raise ValueError('max_cluster_size smaller than grid minimum size')
    for section in ('pca','ica'):
        if section in custom and section!=backend: raise ValueError('Inactive backend section: '+section)
        keys(custom.get(section,{}),defaults[section],section)
    if backend!='umap' and ('umap' in custom or 'execution' in custom):
        raise ValueError('UMAP and ensemble controls do not apply to standalone PCA/ICA')
    configs=[]
    if backend=='umap':
        keys(custom.get('umap',{}),UMAP_KEYS,'umap')
        if 'umap' in custom:
            space={k:parameter_values(v,int if k in ('n_neighbors','n_components','negative_sample_rate','random_state') else None if k in ('metric','densmap') else float) for k,v in {**defaults['umap'],**custom['umap']}.items()}
            configs=[dict(zip(space,vals),config_id='custom_%04d'%i) for i,vals in enumerate(itertools.product(*space.values()),1)]
        else:
            for c in grid['configs']:
                keys(c, {*UMAP_KEYS,'config_id'},'config')
                configs.append({**defaults['umap'],**c})
        for c in configs:
            for key,minimum in [('n_neighbors',2),('n_components',1),('negative_sample_rate',1),('random_state',0)]: integer(c[key],minimum,key)
            if c['random_state']+execution['n_random_states']-1>2**32-1: raise ValueError('Seed exceeds uint32 range')
            for key in ('min_dist','spread','learning_rate','repulsion_strength','local_connectivity','set_op_mix_ratio'):
                if isinstance(c[key],bool) or not isinstance(c[key],(int,float)) or not math.isfinite(c[key]): raise ValueError('Invalid UMAP '+key)
            if not (0<=c['min_dist']<=c['spread'] and c['spread']>0 and c['learning_rate']>0 and c['repulsion_strength']>0 and c['local_connectivity']>=0 and 0<=c['set_op_mix_ratio']<=1): raise ValueError('UMAP parameter outside valid range')
            if c['metric'] not in SUPPORTED_UMAP_METRICS or type(c['densmap']) is not bool: raise ValueError('Invalid UMAP metric or densmap')
    else:
        parameters={**defaults[backend],**custom.get(backend,{})}
        if custom.get(backend,{}).get('retained_components') is not None:
            if custom[backend].get('variance_threshold') is not None: raise ValueError('Conflicting component selection')
            parameters['variance_threshold']=None
        from dimple_representations.pca_runner import _validate_selection
        _validate_selection(parameters['variance_threshold'],parameters['retained_components'])
        if backend=='ica':
            integer(parameters['seed'],0,'ica.seed'); integer(parameters['max_iter'],1,'ica.max_iter')
            if parameters['seed']>2**32-1 or isinstance(parameters['tol'],bool) or not math.isfinite(parameters['tol']) or parameters['tol']<=0: raise ValueError('Invalid ICA seed/tol')
        configs=[{'config_id':backend,**parameters}]
    for c in configs:
        if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]*',c['config_id']): raise ValueError('Unsafe config_id')
    if not configs or len({c['config_id'] for c in configs})!=len(configs): raise ValueError('Empty or duplicate configurations')
    seeds={c['config_id']:list(range(1 if execution['legacy_ensemble_seeds'] else c['random_state'], (1 if execution['legacy_ensemble_seeds'] else c['random_state'])+execution['n_random_states'])) if backend=='umap' else [1] for c in configs}
    return {'backend':backend,'configs':configs,'execution':execution,'hdbscan':hdb,'hdbscan_parameters':hdb_parameters,'seeds':seeds,
            'baseline_config_id':grid['baseline_config_id'] if backend=='umap' and 'umap' not in custom else None}

def resolve_grid(grid,recipe=None):
    keys(grid, {'configs','baseline_config_id','confirmed','input_contract','science'},'run grid')
    if not {'configs','baseline_config_id'}<=set(grid): raise ValueError('Missing recipe fields')
    if recipe is not None and json.dumps({k:grid[k] for k in ('configs','baseline_config_id')},sort_keys=True)!=json.dumps(recipe,sort_keys=True): raise ValueError('Base recipe must match the fixed nine-config recipe; use science for custom settings')
    resolved_science(grid)
    return grid


def hdb_candidates(science, min_samples=None):
    """Stable historical epsilon/min_samples/min_cluster_size order, then extras."""
    grid=science['hdbscan']; extras=science['hdbscan_parameters']
    ordinal=0
    for eps,ms,mcs in itertools.product(grid['cluster_selection_epsilon'],grid['min_samples'],grid['min_cluster_size']):
        for values in itertools.product(*(extras[k] for k in sorted(extras))):
            ordinal+=1
            if min_samples is None or ms==min_samples:
                yield ordinal, {'cluster_selection_epsilon':float(eps),'min_samples':ms,'min_cluster_size':mcs,**dict(zip(sorted(extras),values))}
