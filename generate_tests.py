import os
import openai

# Load API key from environment variable
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Function to generate test cases using OpenAI API
def generate_test_code(source_code, language):
    prompt = f"Generate test cases for the following {language} code:\n\n{source_code}"

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content

# Main function to scan and generate tests
def scan_and_generate_tests():
    SRC_DIR = os.path.join(os.getcwd(), "openAI_testCase_generation/src/")  # Fixed path
    
    if not os.path.exists(SRC_DIR):
        print(f"❌ No source directory found at {SRC_DIR}")
        return
    
    found_files = False
    
    for root, _, files in os.walk(SRC_DIR):
        for file in files:
            if file.endswith((".java", ".js", ".py")):
                found_files = True
                file_path = os.path.join(root, file)
                language = "Java" if file.endswith(".java") else "JavaScript" if file.endswith(".js") else "Python"
                
                with open(file_path, "r", encoding="utf-8") as f:
                    source_code = f.read()

                print(f"📄 Generating tests for {file}...")
                test_code = generate_test_code(source_code, language)
                
                # Generate test file path
                test_file_path = file_path.replace("/src/", "/src/test/").replace(".java", "Test.java").replace(".js", ".test.js").replace(".py", "_test.py")
                os.makedirs(os.path.dirname(test_file_path), exist_ok=True)
                
                with open(test_file_path, "w", encoding="utf-8") as test_file:
                    test_file.write(test_code)
                print(f"✅ Test case written to {test_file_path}")

    if not found_files:
        print("❌ No source files found in src/")

if __name__ == "__main__":
    scan_and_generate_tests()
