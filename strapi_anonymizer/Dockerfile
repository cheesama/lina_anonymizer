FROM strapi/base

WORKDIR /strapi_meta

COPY ./package.json ./
COPY ./yarn.lock ./

RUN yarn install

COPY . .

#ENV NODE_ENV production

RUN yarn build

EXPOSE 1337

CMD ["yarn", "develop"]
