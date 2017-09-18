var myApp = angular.module('project', ['ngRoute']);

myApp.config(function ($routeProvider) {
  $routeProvider
    .when('/', {
      templateUrl: 'static/temp/index.html',
     access: {restricted: true}
    })
     .when('/login', {
      templateUrl: 'static/temp/login.html',
      access: {restricted: false}
    })
    .when('/home', {
      templateUrl: 'static/temp/index.html',
      access: {restricted: true}
    })
    .when('/logout', {
      controller: 'logoutController',
    access: {restricted: true}
    })
    .when('/register', {
      templateUrl: 'static/temp/register.html',
      controller: 'registerController',
      access: {restricted: false}
    })
    .otherwise({
      redirectTo: '/'
    });
});


 myApp.run(function($rootScope,$location, $route, AuthService) {
    $rootScope.$on("$routeChangeStart", function(event, next, current) {
            AuthService.getUserStatus().then(function(){
            //console.log(AuthService.isLoggedIn());
                if (next.access.restricted && !AuthService.isLoggedIn()){
          $location.path('/login');
          $route.reload();
        }

            });
    });
});
