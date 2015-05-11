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
			model.set({"timeDelta": delta})
		});
		this.sort();
	}
	
});

var PostView = Backbone.View.extend({
	
	attributes: {
		class: "row"
	},
	
	render: function(){
		var template = _.template($("#postTemplate").html());
		var html = template(this.model.toJSON());
		this.$el.html(html);
		
		return this;
	}
	
});

var PostsView = Backbone.View.extend({
	
	el: "#container1",
	
	initialize: function() {
		this.render();
	},
	
	render: function(){
		var self = this;
		
		this.model.each(function(post){
			var postView = new PostView({model: post});
			self.$el.append(postView.render().$el);
		});
	}

});

var posts = new Posts();

posts.fetch({
	success: function(){
		successCallback();
	}
});

var successCallback = function(){
	posts.orderByDate()
	var postsView = new PostsView({model: posts})
};