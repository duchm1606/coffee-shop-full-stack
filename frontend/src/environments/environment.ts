/* replace with your variables
 * ensure all variables on this page match your project
 */

export const environment = {
  production: false,
  apiServerUrl: "http://127.0.0.1:5000", // the running FLASK api server url
  auth0: {
    url: "dev-rta7vw0q40ledxrf.us", // the auth0 domain prefix
    audience: "Coffee_shop_labs_apis", // the audience set for the auth0 app
    clientId: "yKeIozTOaCMNUihu16M5YnZDpBhmrfmi", // the client id generated for the auth0 app
    callbackURL: "http://127.0.0.1:4200", // the base url of the running ionic application.
  },
};
