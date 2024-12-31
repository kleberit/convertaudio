from fastapi import FastAPI, UploadFile, File, Query, HTTPException
from fastapi.responses import StreamingResponse
from enum import Enum
import os
import tempfile
from pathlib import Path
import subprocess
import logging

app = FastAPI()

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AudioFormat(str, Enum):
    MP3 = "mp3"
    OGG = "ogg"
    AAC = "aac"

def convert_audio_file(input_path: str, output_path: str, output_format: str):
    """Converter áudio usando FFmpeg diretamente com arquivos"""
    try:
        output_format_str = "adts" if output_format == "aac" else output_format
        
        cmd = [
            'ffmpeg',
            '-i', input_path,
            '-y',  # Sobrescrever arquivo de saída se existir
            '-acodec', 'libmp3lame' if output_format == "mp3" else 'aac' if output_format == "aac" else 'libvorbis',
            output_path
        ]
        
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        stdout, stderr = process.communicate()
        
        if process.returncode != 0:
            logger.error(f"FFmpeg error: {stderr.decode()}")
            raise Exception(f"FFmpeg conversion failed: {stderr.decode()}")
        
        return True
    
    except Exception as e:
        logger.error(f"Conversion error: {str(e)}")
        raise

@app.post("/convert")
async def convert_audio(
    file: UploadFile = File(...),
    output_format: AudioFormat = Query(default=AudioFormat.MP3, description="Formato de saída: mp3, ogg ou aac")
):
    logger.info(f"Recebido arquivo: {file.filename} para conversão para {output_format}")
    
    try:
        # Criar diretório temporário
        with tempfile.TemporaryDirectory() as temp_dir:
            # Salvar arquivo de entrada
            input_path = Path(temp_dir) / file.filename
            with open(input_path, "wb") as buffer:
                content = await file.read()
                buffer.write(content)
            
            # Definir caminho do arquivo de saída
            output_filename = f"converted_{os.path.splitext(file.filename)[0]}.{output_format.value}"
            output_path = Path(temp_dir) / output_filename
            
            # Converter o arquivo
            logger.info(f"Iniciando conversão de {input_path} para {output_path}")
            convert_audio_file(str(input_path), str(output_path), output_format.value)
            
            # Ler o arquivo convertido
            with open(output_path, "rb") as f:
                converted_data = f.read()
            
            logger.info("Conversão concluída com sucesso")
            
            # Retornar o arquivo convertido
            return StreamingResponse(
                iter([converted_data]),
                media_type=f"audio/{output_format.value}",
                headers={
                    "Content-Disposition": f"attachment; filename={output_filename}",
                    "Content-Length": str(len(converted_data))
                }
            )
    
    except Exception as e:
        logger.error(f"Erro durante a conversão: {str(e)}", exc_info=True)
        raise HTTPException(status_code=400, detail=f"Erro na conversão: {str(e)}")

@app.get("/")
async def root():
    return {
        "message": "Audio Converter API",
        "supported_input_formats": [".wav", ".oga", ".ogg", ".mp3"],
        "supported_output_formats": ["mp3", "ogg", "aac"],
        "status": "healthy"
    }
