import subprocess

# Example of a hard-coded secret, which is a security risk
SECRET_KEY = "this_is_a_secret_key"

def insecure_deserialization(data):
    # Insecure deserialization example
    import pickle
    return pickle.loads(data)

def insecure_subprocess_command(user_input):
    # Insecure subprocess call with shell=True, which is vulnerable to shell injection
    command = "echo " + user_input
    subprocess.call(command, shell=True)

def main():
    data = b"cos\nsystem\n(S'echo Hello world!'\ntR."  # Malicious pickle data
    user_input = "user_input_here; rm -rf /"  # Malicious user input

    # Calling functions with security issues
    result = insecure_deserialization(data)
    insecure_subprocess_command(user_input)

    print("Result of insecure deserialization:", result)

if __name__ == "__main__":
    main()
