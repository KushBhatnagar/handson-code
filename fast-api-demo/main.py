from fastapi import FastAPI, File, UploadFile
from os import getcwd
import os
import uvicorn
from fastapi.responses import FileResponse
#added this line to make it work in spyder
import nest_asyncio
nest_asyncio.apply()

app = FastAPI( title="File Management: Upload and Download files",
    description="APIs for uploading and downloading files and images",
    version="0.0.1")
folder_name_list=[]

@app.post("/upload-file/")
async def create_upload_file(uploaded_file: UploadFile = File(...)):
    file_location = f"files/{uploaded_file.filename}"
    folder_path = os.path.splitext(file_location)
    folder_name=os.path.basename(os.path.normpath(folder_path[0]))
    #seting the folder name to pass it to download function
    folder_name_list.append(folder_name)
    with open(file_location, "wb+") as file_object:
        file_object.write(uploaded_file.file.read())
   
    #Test the function call during API execution
    say_hello()
    print("folder name {}".format(folder_name))
    return {"info": f"file '{uploaded_file.filename}' saved at '{file_location}'"}



@app.get("/download/{name_file}")
def download_file(name_file: str):
    return FileResponse(path=getcwd() + "/" + folder_name_list[0] + "/"  + name_file, media_type='application/octet-stream', filename=name_file)


def say_hello():
	print("Hi there!!")

if __name__ == '__main__':
    uvicorn.run(app,host="0.0.0.0", port=8000,log_level="info")
