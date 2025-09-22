import ODRL2SHACL
import sys

print("\nPolicy Comparison Tool.")

print(str(len(sys.argv)))
print(str(sys.argv))

if len(sys.argv) == 5:
    print("\nYou have supplied four arguments. They will be interpreted as:"
          +"\n1) the path to the first policy"
           +"\n2) the path to the second policy"
            +"\n3) the role of the first policy"
             +"\n4) the role of the second policy\n")
    first_policy = sys.argv[1]
    second_policy = sys.argv[2]
    first_policy_role = sys.argv[3]
    second_policy_role = sys.argv[4]
else:
    print("\nYou have not supplied four arguments (path to the first policy, path to the second policy, role of the first policy, role of the second policy).")
    print("\nStarting interactive input collection...\n")
    first_policy = input("\nEnter the path to the first policy file: ")

    second_policy = input("\nEnter the path to the second policy file: ")

    first_policy_role = input("\nThe role of the first policy can be set to either 'any', 'requester' or `provider'. "
                              + "\nThe role of the second policy will then be automatically set to 'any', 'provider' or `requester'."
                              + "\nIf the submitted string will not match any of the valid strings, it will default to 'any'."
                              + "\nEnter the role of the first policy: ")
    second_policy_role = 'any'

    if first_policy_role == 'requester':
        second_policy_role = 'provider'
    elif first_policy_role == 'provider':
        second_policy_role = 'requester'
    elif first_policy_role != 'any':
        first_policy_role = 'any'

print("Path to the first policy:", first_policy)
print("Path to the second policy:", second_policy)

print("Role of the first policy:", first_policy_role)
print("Role of the second policy:", second_policy_role)

print("\nParsing the ODRL files and producing the conflict report...\n")

with open(first_policy, 'r') as file:
    first_policy_data = file.read()
with open(second_policy, 'r') as file:
    second_policy_data = file.read()

json_result = ODRL2SHACL.compare_policies_from_string(first_policy_data,second_policy_data,first_policy_role,second_policy_role)

print(json_result)

# python .\compare_policies.py .\example_policies\example_strict.json .\example_policies\example_permissive.json requester provider
