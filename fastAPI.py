from fastapi import FastAPI, Request, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi import Form


from typing import List
import os
import Vegetation_indices
import Cut_to_polygon_MT

app = FastAPI()


# Ustawienie folderu statycznego dla plików CSS, JS, itp.
app.mount("/static", StaticFiles(directory="static"), name="static")

# Ustawienie szablonów Jinja2
templates = Jinja2Templates(directory="templates")

def run_vegetation_indices():
    Vegetation_indices.main()
    # Dodaj tutaj kod, który ma być wykonany po zakończeniu run_vegetation_indices

def run_cut_to_polygon(input_vector: str, input_raster: str, output_dir: str, files: List[UploadFile] = File(...)):
    Cut_to_polygon_MT.main(input_vector, input_raster, output_dir)
    # Dodaj tutaj kod, który ma być wykonany po zakończeniu run_cut_to_polygon

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/run_vegetation_indices")
def run_vegetation_indices_endpoint():
    run_vegetation_indices()
    print("Operacja run_vegetation_indices została wykonana.")
    return {"message": "Successfully executed vegetation indices."}

@app.post("/run_cut_to_polygon")
def run_cut_to_polygon_endpoint(request: Request, input_vector: str = Form(...), input_raster: str = Form(...), output_dir: str = Form(...), files: List[UploadFile] = File(...)):
    run_cut_to_polygon(input_vector, input_raster, output_dir, files)
    print("Operacja run_cut_to_polygon została wykonana.")
    return {"message": "Successfully executed cut to polygon."}

