FROM node:14

WORKDIR /app
COPY package.json .
COPY tsconfig.json .
RUN npm install
COPY ./src ./src

RUN npm install -g typescript

RUN tsc
EXPOSE 3000

CMD ["node", "dist/main.js"]
