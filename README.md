import subprocess

# Define the Java command
java_command = ['java', '-classpath', 'com/java', 'abc', 'kyvos_admin', 'kyvos_password']

# Loop through the DataFrame indices
for i in dfRules.index:
    strExistingRules = dictRow.get(dfRules['RULE_NAME'][i])
    if strExistingRules:
        # Run the Java code with parameters
        subprocess.run(java_command, check=True)
