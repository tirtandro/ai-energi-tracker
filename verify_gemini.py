import os
import ecologits
from ecologits import EcoLogits

try:
    from google import genai
    GOOGLE_GENAI_AVAILABLE = True
except ImportError:
    GOOGLE_GENAI_AVAILABLE = False

def verify():
    print(f"EcoLogits version: {ecologits.__version__}")
    
    if not GOOGLE_GENAI_AVAILABLE:
        print("ERROR: google-genai is not installed.")
        return

    print("google-genai is installed.")
    
    # Initialize EcoLogits
    EcoLogits.init(providers=["google_genai"])
    print("EcoLogits initialized with google_genai provider.")
    
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key or api_key == "<GEMINI_API_KEY>":
        print("WARNING: GEMINI_API_KEY not found in environment. Skipping live test.")
        return

    print("GEMINI_API_KEY found. Running live test...")
    client = genai.Client(api_key=api_key)
    
    models_to_try = ["gemini-3-flash-preview", "gemini-2.0-flash"]
    
    for model_name in models_to_try:
        print(f"Testing model: {model_name}...")
        try:
            response = client.models.generate_content(
                model=model_name,
                contents="Say 'EcoLogits is ready!'"
            )
            print(f"Response received successfully from {model_name}.")
            if hasattr(response, 'impacts'):
                print(f"Impacts: {response.impacts}")
                try:
                    print(f"Energy: {response.impacts.energy.value.mean} kWh")
                except AttributeError:
                    print(f"Impacts summary: {response.impacts}")
                print(f"SUCCESS: EcoLogits correctly tracked the impact for {model_name}.")
                return # Exit after first successful call
            else:
                print(f"FAILURE: Response object from {model_name} does not have 'impacts' attribute.")
        except Exception as e:
            if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                print(f"QUOTA EXHAUSTED for {model_name}. Attempting fallback...")
                continue
            else:
                print(f"ERROR during test with {model_name}: {e}")
                break

    print("All attempts failed or quota reached for all models.")

if __name__ == "__main__":
    verify()
