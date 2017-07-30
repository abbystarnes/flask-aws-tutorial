(function () {
  angular.module('app')
  .service('PostService', ['$http', function service($http) {
    const se = this;
    se.posts = [];

    se.getPosts = function getPosts() {
      return $http.get('/api/posts').then((res) => {
        se.posts = res.data;
      });
    };

    se.addPost = function addPost(post) {
      return $http.post('/api/posts', post).then((res) => {
        console.log('making post request');
        console.log(res.data, 'data?');
        se.posts.push(res.data);
      });
    };

    se.deletePost = function deletePost(post) {
      return $http.delete(`/api/posts/${post.id}`).then((res) => {
        const index = se.posts.indexOf(post);
        se.posts.splice(index, 1);
      });
    };

    se.editPost = function editPost(postID, updated) {
      return $http.patch(`api/posts/${postID}`, updated).then((res) => {
        se.posts.forEach((post) => {
          if (parseInt(post.id) === parseInt(postID)) {
            const index = se.posts.indexOf(post);
            se.posts.splice(index, 1, updated);
          }
        });
      });
    };

    se.upVote = function upVote(post) {
      return $http.post(`api/posts/${post.id}/votes`).then((res) => {
        const index = se.posts.indexOf(post);
        se.posts[index].vote_count += 1;
      });
    };

    se.downVote = function upVote(post) {
      return $http.delete(`api/posts/${post.id}/votes`).then((res) => {
        const index = se.posts.indexOf(post);
        se.posts[index].vote_count -= 1;
      });
    };
  }]);
}());
