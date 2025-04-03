# Usa uma imagem leve do Node.js 
FROM node:18-alpine

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia apenas os arquivos de dependências primeiro
COPY package.json package-lock.json ./

# Instala as dependências
RUN npm install --legacy-peer-deps

# Copia o restante dos arquivos do projeto
COPY . .

# Expõe a porta 5173 para o React
EXPOSE 5173

# Inicia o servidor React
CMD ["npm", "run", "dev", "--", "--host"]
