(function () {
  angular.module('app')

  .config(['$stateProvider', '$urlRouterProvider', '$locationProvider', function ($stateProvider, $urlRouterProvider, $locationProvider) {
    $locationProvider.html5Mode(true);
    $stateProvider
    .state({ name: 'edit', url: '/posts/:id/edit', component: 'controls' })
    .state({ name: 'posts', url: '/posts/', component: 'controls' })
    .state({ name: 'add', url: '/posts/add', component: 'controls' });
  }]);
}());
