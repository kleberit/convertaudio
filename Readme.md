Audio Converter API
Uma API robusta para conversão de arquivos de áudio entre diferentes formatos, utilizando FFmpeg.

Formatos Suportados
Entrada
WAV
OGA/OGG
MP3
Saída
MP3
OGG
AAC
Uso
Docker
Para executar a API usando Docker:

bash
Copiar

docker pull seu-usuario/audio-converter:latest
docker run -p 9596:8000 seu-usuario/audio-converter:latest
A API estará disponível em http://localhost:9596.

API Endpoints
POST /convert: Converter arquivo de áudio
Parâmetros:
file: O arquivo de áudio a ser convertido (multipart/form-data)
output_format: O formato de saída desejado (query parameter, valores: mp3, ogg, aac)
Exemplo de uso com curl:
bash
Copiar

    curl -X POST -F "file=@path/to/audio.wav" "http://localhost:9596/convert?output_format=mp3" --output converted.mp3
GET /: Informações da API
Desenvolvimento
Requisitos
Python 3.9+
FFmpeg
Docker (opcional)
Instalação
Clone o repositório:
bash
Copiar

   git clone https://github.com/seu-usuario/audio-converter.git
   cd audio-converter
Instale as dependências:
bash
Copiar

   pip install -r requirements.txt
Certifique-se de que o FFmpeg está instalado em seu sistema.
Execução Local
Para executar a API localmente:

bash
Copiar

uvicorn main:app --host 0.0.0.0 --port 8000
Construindo a Imagem Docker
Para construir a imagem Docker localmente:

bash
Copiar

make build
Versionamento
O projeto segue Semantic Versioning.

Para criar uma nova versão:

Atualize o código conforme necessário.
Execute make bump-version e insira a nova versão.
Atualize o CHANGELOG.md com as alterações.
Execute make all para construir, taguear e publicar a nova versão.
Contribuindo
Contribuições são bem-vindas! Por favor, siga estes passos:

Fork o repositório
Crie uma branch para sua feature (git checkout -b feature/AmazingFeature)
Commit suas mudanças (git commit -m 'Add some AmazingFeature')
Push para a branch (git push origin feature/AmazingFeature)
Abra um Pull Request
Licença
Distribuído sob a licença MIT. Veja LICENSE para mais informações.