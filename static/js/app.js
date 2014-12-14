var app = app || {};
$(function(){
var fakePatient = new app.patientModel();

////////////////////////////////////////////////////////////
// BASIC DEMOGRAPHICS
////////////////////////////////////////////////////////////
var mrn = new app.resultModel({ displayName: "MRN", resultValue: "12345678" });
var loc = new app.resultModel({ displayName: "Location", resultValue: "7B 22-1" });
var iso = new app.resultModel({ displayName: "Isolation", resultValue: "MRSA" });
var demview = new app.resultCollectionView({ collection: new app.orderCollection([mrn,loc,iso]), el: $("#demographics table")})
demview.render();


////////////////////////////////////////////////////////////
// BASIC RESULTS
////////////////////////////////////////////////////////////
var weight = new app.resultModel({ displayName: "Weight", resultValue: "70 kg" });
var allergies = new app.resultModel({ displayName: "Allergies", resultValue: "NKA" });
var egfr = new app.resultModel({ displayName: "eGFR", resultValue: ">60 ml/min" });
var qtc = new app.resultModel({ displayName: "QTc", resultValue: "425 ms" });
var lvef = new app.resultModel({ displayName: "LVEF", resultValue: "30%" });
var a1c = new app.resultModel({ displayName: "A1c", resultValue: "6.2%" });
var basicResults = new app.resultCollection([weight, allergies, egfr, qtc, lvef, a1c]);
var basicResultsView = new app.resultCollectionView({ collection: basicResults, el: $("#basicResults table") });
basicResultsView.render(); 

////////////////////////////////////////////////////////////
// BASIC ORDERS
////////////////////////////////////////////////////////////
var basicOrders = new app.orderCollection([diet, axs, foley, code, pt, nutrition, socialwork]);
var basicOrdersView = new app.orderWithTitleCollectionView({ collection: basicOrders, el: $("#basicOrders table") });
basicOrdersView.render();

////////////////////////////////////////////////////////////
// BASIC MED ORDERS
////////////////////////////////////////////////////////////
var basicMedOrders = new app.orderCollection([insulin, vte, gi, ivf]);
var basicMedOrdersView = new app.orderWithTitleCollectionView({ collection: basicMedOrders, el: $("#basicMedOrders table") });
basicMedOrdersView.render();

////////////////////////////////////////////////////////////
// PROBLEMS
////////////////////////////////////////////////////////////
$('#problems').append( problem1view.render().el );

var metoprolol = new app.orderModel({ displayName: "IVF", category: MEDICINE, tags: ["cad", "beta blocker"], displayName: "Metoprolol 12.5 mg po q6h"})
var asa = new app.orderModel({ displayName: "IVF", category: MEDICINE, tags: ["asa", "cad", "antiplatelet"], displayName: "Aspirin 81 mg po qd", modifier: HOLD})
var atorvastatin = new app.orderModel({ displayName: "IVF", category: MEDICINE, tags: ["ivf"], displayName: "Atorvastatin 80 mg po qd"})
var cadOrders = new app.orderCollection([metoprolol, asa, atorvastatin]);
var cadPlan = new app.planCollection();
cadPlan.addOrders(cadOrders);
var problem2 = new app.problemModel({ title: "CAD", 
	medicalDecisionMaking: "Stable, no ekg changes.",
	plan: cadPlan });
var problem2view = new app.problemView({ model: problem2 });
$('#problems').append( problem2view.render().el );

var renaldose = new app.orderModel({ category: MEDICINE, displayName:"Renally dose medications" });
var akiOrders = new app.orderCollection([ivf, renaldose]);
var akiPlan = new app.planCollection();
akiPlan.addOrders(akiOrders);
var problem3 = new app.problemModel({ title: "AKI", 
	medicalDecisionMaking: "Likely prerenal",
	plan: akiPlan });
var problem3view = new app.problemView({ model: problem3 });
$('#problems').append( problem3view.render().el );


//var pc = new app.problemCollection([problem1, problem2, problem3]);

app.datamodel = new app.dataModel();
app.dataview = new app.dataView({ el: $(".data"), model: app.datamodel});
app.dataview.render();

var v = new app.orderView({ model : insulin });
$('body').html( v.render().el );

var div = $('<div contenteditable="true" style="width:400px;border:thin solid;height:400px"></div>')

div.keyup(function(){
	var html = div.html();

	html.replace("david", '<span style="color:orange">david</span>');

	div.html(html);

})

$('body').html(div);

});