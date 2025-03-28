# main.py
from fastapi import FastAPI, File, UploadFile
import uvicorn
import os
import uuid
from audio_processing import extract_features
from topsis import topsis_score
from conversion import convert_webm_to_wav
from logger import log_info, log_error
app = FastAPI()

# In-memory store of all feature vectors
all_features_store = []

@app.post("/evaluate")
async def evaluate_singing(file: UploadFile = File(...)):
    log_info(f"Request received: Evaluating file '{file.filename}'")
    
    # Create a temporary directory if it doesn't exist
    temp_dir = os.path.join(os.getcwd(), "temp_files")
    os.makedirs(temp_dir, exist_ok=True)
    
    # Use absolute paths for temp files
    temp_filename = os.path.join(temp_dir, f"{uuid.uuid4()}_{file.filename}")
    log_info(f"Step 1: Saving uploaded file to '{temp_filename}'")
    
    with open(temp_filename, 'wb') as f:
        content = await file.read()
        f.write(content)
    log_info(f"File saved successfully ({len(content)} bytes)")

    # 2. Check file extension and convert if necessary
    log_info(f"Step 2: Checking file format and converting if needed")
    if temp_filename.endswith(".webm"):
        try:
            
            # Check if file exists before conversion
            if not os.path.exists(temp_filename):
                log_info(f"File not found 101: {temp_filename}")

                raise FileNotFoundError(f"The file {temp_filename} does not exist")
                
            log_info(f"Converting WEBM to WAV format")
            converted_filename = convert_webm_to_wav(temp_filename)
            log_info(f"Conversion successful: '{converted_filename}'")
            
            # Verify converted file exists
            if not os.path.exists(converted_filename):
                raise FileNotFoundError(f"Conversion did not produce the expected file: {converted_filename}")
        except Exception as e:
            log_error(f"Conversion failed: {str(e)}")
            if os.path.exists(temp_filename):
                os.remove(temp_filename)
            return {"error": f"Conversion failed: {str(e)}"}
    else:
        log_info(f"No conversion needed, using original file")
        converted_filename = temp_filename

    # 3. Extract features from the converted file
    log_info(f"Step 3: Extracting audio features from '{converted_filename}'")
    try:
        features_dict = extract_features(converted_filename)
        feature_vec = [
            features_dict["mean_pitch"],
            features_dict["tempo"],
            features_dict["tempo_consistency"],
            features_dict["pitch_quality"],
            features_dict["pace"]
        ]
        log_info(f"Features extracted: {features_dict}")
    except Exception as e:
        log_error(f"Feature extraction failed: {str(e)}")
        # Clean up files
        if os.path.exists(temp_filename):
            os.remove(temp_filename)
        if converted_filename != temp_filename and os.path.exists(converted_filename):
            os.remove(converted_filename)
        return {"error": f"Feature extraction failed: {str(e)}"}

    # 4. Store features and compute TOPSIS score
    log_info(f"Step 4: Computing TOPSIS score")
    log_info(f"Total samples in database: {len(all_features_store)}")
    all_features_store.append(feature_vec)
    score, rank = topsis_score(feature_vec, all_features_store)
    log_info(f"TOPSIS calculation complete. Score: {score}, Rank: {rank}")

    # 5. Clean up temporary files
    log_info(f"Step 5: Cleaning up temporary files")
    if os.path.exists(temp_filename):
        os.remove(temp_filename)
    if converted_filename != temp_filename and os.path.exists(converted_filename):
        os.remove(converted_filename)
    log_info(f"Cleanup complete")

    # Return results
    log_info(f"Response: Score: {score}, Rank: {rank}")
    return {"score": score, "rank": rank}

@app.get("/")
async def root():
    log_info("Health check endpoint accessed")
    return {"status": "Singing evaluation API is running"}

if __name__ == "__main__":
    log_info("Starting server...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
