(function () {
  angular.module('app')
  .service('CommentService', ['$http', function service($http) {
    const se = this;

    se.getComments = function getComments(post) {
      return $http.get(`/api/posts/${post}/comments`).then((res) => {
        se.comments = res.data;
      });
    };

    se.addComment = function addComment(post, updated) {
      return $http.post(`/api/posts/${post}/comments`, updated).then(res => res.data);
    };

    se.deleteComment = function deleteComment(post, comment) {
      return $http.delete(`/api/posts/${post}/comments/${comment}`).then(res => res.data);
    };

    se.editComment = function editComment(comment, updated) {
      return $http.patch(`/api/posts/${comment.post_id}/comments/${comment.id}`, updated).then(res => res.data);
    };
  }]);
}());
