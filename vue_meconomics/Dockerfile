#client vue Dockerfile
FROM node:14.17.5 as build-stage
WORKDIR /vue_meconomics
COPY package*.json ./
RUN npm install
COPY ./ .
ARG DEV=false
RUN if [ "$DEV" = "false" ] ; then npm run build ; fi
EXPOSE 8095
CMD [ "npm", "run", "serve" ]
