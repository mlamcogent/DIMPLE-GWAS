// Supply a generated context and frozen identity arguments; never build the workspace root.
variable "DIMPLE_CONTEXT" { default = "" }
variable "DIMPLE_SOURCE_SHA256" { default = "" }
variable "DIMPLE_WHEEL_SHA256" { default = "" }
variable "DIMPLE_LOCK_SHA256" { default = "" }
variable "DIMPLE_SOURCE_DATE_EPOCH" { default = "" }
variable "DIMPLE_RUNTIME_TAG" { default = "" }
variable "DIMPLE_TEST_TAG" { default = "" }

group "current" { targets = ["freeze3-current-runtime"] }
group "validation" { targets = ["freeze3-current-test"] }
// A two-image release group is intentionally withheld until the historical-lane conflict is resolved.

target "common" {
  context = DIMPLE_CONTEXT
  dockerfile = "Dockerfile"
  platforms = ["linux/amd64"]
  network = "none"
  args = {
    SOURCE_SHA256 = DIMPLE_SOURCE_SHA256
    WHEEL_SHA256 = DIMPLE_WHEEL_SHA256
    LOCK_SHA256 = DIMPLE_LOCK_SHA256
    SOURCE_DATE_EPOCH = DIMPLE_SOURCE_DATE_EPOCH
  }
}
target "freeze3-current-runtime" {
  inherits = ["common"]
  target = "freeze3-current-runtime"
  tags = [DIMPLE_RUNTIME_TAG]
}
target "freeze3-current-test" {
  inherits = ["common"]
  target = "freeze3-current-test"
  tags = [DIMPLE_TEST_TAG]
}
