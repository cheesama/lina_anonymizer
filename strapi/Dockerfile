FROM strapi/base

ARG STRAPI_VERSION
RUN yarn global add strapi@${STRAPI_VERSION}

RUN mkdir /srv/app && chown 1000:1000 -R /srv/app

WORKDIR /srv/app
COPY strapi_anonymizer/.tmp             .tmp
COPY strapi_anonymizer/api              api
COPY strapi_anonymizer/build            build
COPY strapi_anonymizer/config           config
COPY strapi_anonymizer/extensions       extensions
COPY strapi_anonymizer/node_modules     node_modules
COPY strapi_anonymizer/package.json    package.json
COPY strapi_anonymizer/public           public
COPY strapi_anonymizer/yarn.lock        yarn.lock

#VOLUME /srv/app

CMD ["strapi", "develop"]
