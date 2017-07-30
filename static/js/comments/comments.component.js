(function () {
  angular.module('app')
  .component('comments', {
    bindings: {
      post: '<',
    },
    controller,
    templateUrl: 'static/js/comments/comments.template.html',
  });
  controller.$inject = ['CommentService'];

  function controller(CommentService) {
    const vm = this;
    vm.comments = [];
    vm.updatedComment = {};

    vm.$onInit = function () {
      vm.getComments();
    };

    vm.getComments = function () {
      CommentService.getComments(vm.post.id).then((result) => {
        vm.comments = CommentService.comments;
      });
    };

    vm.addComment = function () {
      CommentService.addComment(vm.post.id, vm.comment).then((result) => {
        vm.getComments();
        delete vm.comment;
        vm.commentForm.$setUntouched();
      });
    };

    vm.deleteComment = function (comment) {
      CommentService.deleteComment(vm.post.id, comment.id).then(() => {
        vm.getComments();
      });
    };

    vm.editComment = function (comment) {
      CommentService.editComment(comment, vm.updatedComment).then(() => {
        vm.getComments();
        vm.editing = false;
      });
    };

    vm.editingComment = function (comment) {
      if (vm.editing === comment.id) {
        vm.editing = '';
      } else {
        vm.editing = comment.id;
        vm.updatedComment = JSON.parse(JSON.stringify(comment));
      }
    };
  }
}());
