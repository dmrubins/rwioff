var app = app || {};

app.orderCollection = Backbone.Collection.extend({
	comparator : function(a, b){
		if ( a.get('category') > b.get('category') ){
			return 1;
		}else if ( a.get('category') < b.get('category') ){
			return -1;
		}else{
			return a.get('displayName') > b.get('displayName');
		}
	}
});