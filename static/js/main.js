var Post = Backbone.Model.extend({
	
	urlRoot: "/posts"

});

var Posts = Backbone.Collection.extend({
	
	model: Post,
	
	url: "/posts",
	
	comparator: "timeDelta",
	
	orderByDate: function(){
		this.forEach(function(model){
			var splitDate = model.attributes.Date.split('/');
			var newDate = splitDate[1] + '/' + splitDate[0] + '/' + splitDate[2];
			var delta = Date.parse(newDate);
			delta = delta * -1;
			model.set({"timeDelta": delta});
		});
		this.sort();
		
		return this;
	}
	
});

var PostView = Backbone.View.extend({
	
	attributes: {
		class: "row"
	},
	
	events: {
		"click #delete": "onClickDelete"
	},
	
	onClickDelete: function(event){
		event.preventDefault();
		this.model.destroy();
	},
	
	render: function(){
		if (this.model.attributes.id == 0) {
			this.$el.attr("id", this.model.id);
		} else {
			this.$el.attr("id", this.model.id || counter);
		};
		
		var template = _.template($("#postTemplate").html());
		var html = template(this.model.toJSON());
		this.$el.html(html);
		
		return this;
	}
	
});

var PostsView = Backbone.View.extend({
	
	el: "body",
	
	initialize: function() {
		this.render();
		
		this.model.on("add", this.onAddPost, this);
		this.model.on("remove", this.onRemovePost, this);
	},
	
	events: {
		"click #postButton": "onClickAdd"
	},
	
	onClickAdd: function() {
		var $name = $("#name")
		var $email = $("#email")
		var $text = $("#comment")
		var todaysDate = this.getDate();
		
		var newPost = new Post({Name: $name.val(), Email: $email.val(), Date: todaysDate, Text: $text.val()});
		
		if (newPost.attributes.Name && newPost.attributes.Email && newPost.attributes.Text) {
			this.model.add(newPost);
			newPost.save();
			$name.val(""); 
			$email.val(""); 
			$text.val("");
		} else {
			alert("Please fill out all the required fields...");
		};
	},
	
	getDate: function() {
		var today = new Date();
		var dd = today.getDate();
		var mm = today.getMonth() + 1; 

		var yy = today.getFullYear();
		yy = yy.toString();
		yy = yy.substring(2, 4);
		
		if (dd < 10) {
			dd = '0' + dd
		};
		if (mm < 10) {
			mm = '0' + mm
		}; 
		
		var today = dd + '/' + mm + '/' + yy;
		
		return today;
	},
	
	onAddPost: function(post) {
		var newPostView = new PostView({model: post});
		$("#container1").prepend(newPostView.render().$el);
	},
	
	onRemovePost: function(removedPost){
		this.$("div #" + removedPost.id).remove();
	},
	
	render: function(){
		var self = this;
		
		this.model.each(function(post){
			var postView = new PostView({model: post});
			$("#container1").append(postView.render().$el);
		});
	}

});

var counter = 0;
var posts = new Posts();

posts.fetch({
	success: function(){
		successCallback();
	}
});

var successCallback = function(){
	posts.orderByDate();
	var postsView = new PostsView({model: posts})
	counter = get_highest_model_id()
};

function get_highest_model_id() {
	var highest_id = 0;
	
	for (var i = 0; i < posts.length; i++) {
		if (posts.at(i).attributes.id > highest_id) {
			highest_id = posts.at(i).attributes.id
		};
	};
	
	return highest_id + 1
};