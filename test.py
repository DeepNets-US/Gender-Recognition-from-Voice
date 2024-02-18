import subprocess

audio_file_path = input("File path: ")

r_script_result = subprocess.run(['Rscript', 'voice_analysis.R', audio_file_path], capture_output=True, text=True)
if r_script_result.returncode != 0:
    print("Error:", r_script_result.stderr)

# Display R script output (audio features)
print("R script output:", r_script_result.stdout)