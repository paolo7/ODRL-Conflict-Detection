# ODRL Conflict Detection between Policies

This repository contains python functions to compare two ODRL policies. 

In the current version, this is done by creating a SHACL graph that validates other policies and
returns validation errors on policies that conflict with the original one.

## Semantics

Policies are associated with 2 roles: *requester* and *provider*. 
A conflict is detected if the requester policy is not equivalent or more restrictive
than the provider one. 

## Requirements

Required libraries:
* rdflib
* pyshacl

## Instructions

After installing the requirements, you can run the `compare_policies.py` file to compare two policies.

If you run this code without arguments, it will ask you about the file path to the two policies to compare, 
and their roles, using in-line inputs.

If you run it with four arguments, it will automatically run the policy comparison and return the result.
The four arguments it expects are:
1. The path to the first policy
2. The path to the second policy
3. The role of the first policy
4. The role of the second policy

For example, using the provided sample policies you can run the following command to verify that the stricter policy does not 
conflict with the more permissive one, if the permissive one is the one of the provider. If you swap the roles (or the 
policies), it will detect a conflict.
```
python .\compare_policies.py .\example_policies\example_strict.json .\example_policies\example_permissive.json requester provider
```


## Programmatic Usage Instructions

To compare two policies from Python, call the `compare_policies` or the `compare_policies_from_string` functions in `ODRL2SHACL.py`.
This `compare_policies_from_string` function takes two mandatory arguments: the first two are two string serialisations of ODRL in one of the following 
formats: 'json-ld', 'turtle', 'xml', 'nt', 'n3', 'trig', 'nquads'. The remaining two optional arguments, `role_one` and 
`role_two` are one of the following strings "any", "requester", "provider". You can either set one role as provider and 
one as requester, to check whether the requester policy is strictier than the provider, or set both to "any" to consider
both cases. If the "any" role is chosen, this function effectively checks for equivalence of the two policies. The
`compare_policies` function behaves exactly the same but takes two rdflib graph objects instead of their string serialisation.

The `compare_policies` function returns a JSON object that follows this schema:
```
{ 
  "$schema": "https://json-schema.org/draft/2020-12/schema", 
  "type": "object", 
  "properties": { 
    "conflict_status": { "type": "string" }, 
    " p_one_id": { "type": "string" }, 
    " p_two_id": { "type": "string" }, 
    " p_one_role": { "type": "string" }, 
    " p_two_role": { "type": "string" }, 
    "conflict_set": { 
      "type": "array", 
      "items": { 
        "type": "object", 
        "properties": { 
          "conflicting_rules_in_p_one": { 
            "type": "array", 
            "items": { "type": "string" }, 
            "uniqueItems": true 
          }, 
          "conflicting_rules_in_p_two": { 
            "type": "array", 
            "items": { "type": "string" }, 
            "uniqueItems": true 
          }, 
          "conflict_explanation": { 
            "oneOf": [{ "type": "string" }, { "type": "object" }] 
          } 
        }, 
        "required": ["conflicting_rules_in_p_one", "conflicting_rules_in_p_two", "conflict_explanation"] 
      }, 
      "uniqueItems": true 
    } 
  }, 
"required": ["conflict_status", "p_one_id", "p_two_id"] 
} 
```

Other files:
* `examples.py` contains example policies, and defines cases where a match or a conflict should occur
* `tests.py` uses the examples in `examples.py` to perform automated tests of the core functionality
* `main.py` is a sample script that uses the core functionalities

## Limitations 

Policy objects are supposed to be ODRL turtle files,
with the following restrictions:
* Each turtle file should contain a single Policy object
* It supports the following features: 
  * action
  * target
  * assignee
  * assigner
  * purpose (this is not a standard ODRL feature, but an optional addition)

Refinements and constraints are currently not supported



