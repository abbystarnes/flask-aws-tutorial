(function () {
  angular.module('app')
  .component('post', {
    bindings: {
      post: '<',
    },
    controller,
    templateUrl: 'static/js/posts/post.template.html',
  });

  controller.$inject = ['PostService'];

  function controller(PostService) {
    const vm = this;

    vm.deletePost = function () {
      PostService.deletePost(vm.post).then((result) => {
        delete vm.post;
      });
    };

    vm.upVote = function () {
      PostService.upVote(vm.post).then(() => {
        vm.posts = PostService.posts;
        vm.voteStatus();
      });
    };

    vm.downVote = function () {
      PostService.downVote(vm.post).then(() => {
        vm.posts = PostService.posts;
        vm.voteStatus();
      });
    };

    vm.voteStatus = function () {
      if (vm.post.vote_count > 0) {
        return true;
      }
      return false;
    };

    vm.favorite = function (post, bool) {
      post.favorite = !post.favorite;
    };
  }
}());
