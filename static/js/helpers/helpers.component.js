(function () {
  angular.module('app')
  .component('controls', {
    controller,
    templateUrl: 'static/js/helpers/helpers.template.html',
  });

  controller.$inject = ['PostService', '$stateParams', '$state'];

  function controller(PostService, $stateParams, $state) {
    const vm = this;
    vm.posts = [];
    vm.updatedPost = {};
    vm.votes = 'votes';
    vm.date = 'date';
    vm.title = 'title';

    vm.$onInit = function () {
      vm.sort('vote_count', 'true');
      vm.filter = '';
      vm.activeItem = 'votes';
      vm.getPosts();
    };

    vm.getPosts = function () {
      PostService.getPosts().then((result) => {
        vm.posts = PostService.posts;
      }).then(() => {
        if ($stateParams.id) {
          vm.openEdit($stateParams.id);
        }
        if ($state.current.name === 'add') {
          vm.postOpen = true;
        }
      });
    };

    vm.addPost = function () {
      vm.post.votes = 0;
      PostService.addPost(vm.post).then(() => {
        delete vm.post;
        vm.postForm.$setUntouched();
        vm.postOpen = false;
        $state.go('posts');
      });
    };

    vm.editPost = function () {
      PostService.editPost($stateParams.id, vm.updatedPost).then(() => {
        $state.go('posts');
      });
    };

    vm.openEdit = function (postID) {
      vm.posts.forEach((post) => {
        if (parseInt(post.id, 10) === parseInt(postID, 10)) {
          vm.updatedPost = JSON.parse(JSON.stringify(post));
        }
      });
      vm.editingOpen = true;
    };

    vm.sort = function (cat, reverse) {
      vm.sortCat = cat;
      vm.reverseSort = reverse;
    };

    vm.setActive = function (e) {
      vm.activeItem = e.target.id;
    };
  }
}());
