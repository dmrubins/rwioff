var app = app || {};

var diet = new app.orderModel({ title: "Diet", category: GENERAL_CARE, tags: ["diet"], displayName: "NPO"})
var axs = new app.orderModel({ title: "Access", category: GENERAL_CARE, tags: ["access", "iv", "tubes"], displayName: "PIV x 2"})
var foley = new app.orderModel({ title: "Foley", category: GENERAL_CARE, tags: ["foley", "tubes"], displayName: "None"})
var code = new app.orderModel({ title: "Code", category: GENERAL_CARE, tags: ["code"], displayName: "Full (Confirmed)"})
var pt = new app.orderModel({ title: "PT", category: CONSULT, tags: ["physical therapy"], displayName: "Consulted"})
var nutrition = new app.orderModel({ title: "Nutrition", category: CONSULT, tags: ["nutrition"], displayName: "None"})
var socialwork = new app.orderModel({ title: "Social Work", category: CONSULT, tags: ["social work"], displayName: "None"})
var insulin = new app.orderModel({ title: "Insulin", category: MEDICINE, tags: ["insulin", "diet", "DM"], displayName: "Lantus 16 U qhs"})
var vte = new app.orderModel({ title: "VTE PPX", category: MEDICINE, tags: ["vte", "ppx"], displayName: "None"})
var gi = new app.orderModel({ title: "GI PPX", category: MEDICINE, tags: ["gi", "ppx"], displayName: "Protonix 8 mg/hr"})
var ivf = new app.orderModel({ title: "IVF", category: MEDICINE, tags: ["ivf"], displayName: "NS 100 cc/hr x 12 hrs"})

//////////////////////////////////////
// RESULTS
//////////////////////////////////////
var cbc_r = new app.resultModel({displayName: "Hct", resultValue: "21"});
var gi_r = new app.resultModel({displayName: "GI Consult", resultValue: "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque pellentesque odio quis libero consectetur egestas. Etiam egestas elementum dolor, id aliquam enim venenatis eu. Quisque feugiat gravida dolor, ut tincidunt eros porta et. Nunc quis urna ut magna placerat gravida a in urna. In sit amet tincidunt tellus, quis varius nisi. Nullam eget enim nisl. Sed vestibulum commodo dignissim. Vivamus ornare ligula nec nulla placerat iaculis. Mauris at ex elit. Vestibulum a pulvinar elit. Nullam justo neque, mollis nec molestie nec, fermentum at sem. Ut sodales neque id ante placerat, et elementum nisl faucibus."});

//////////////////////////////////////
// ORDERS 
//////////////////////////////////////
var cbc_o = new app.orderCollection([new app.orderModel({displayName: "CBC", category:LAB_ORDER, results : new app.resultCollection([cbc_r])})])
var cbc_p = new app.planModel({freeForm: "Trend #order", associatedOrders: cbc_o})

var giconsult = new app.orderModel({category: CONSULT, displayName: "GI Consult", results : new app.resultCollection([gi_r])})
//var ugibOrders = new app.orderCollection([diet, ivf, axs, gi, giconsult]);
//var ugibOrders = new app.orderCollection([diet]);
//var tands = new app.planModel({freeForm: "Type and Screen"})
var ugibPlan = new app.planCollection([cbc_p])
ugibPlan.addOrder(diet);
ugibPlan.addOrder(giconsult);
ugibPlan.addOrder(gi);
var problem1 = new app.problemModel({ title: "UGIB", 
	medicalDecisionMaking: "Pt presented with melena, blah, blah, blah. Most likely to be an upper GI source.",
	plan: ugibPlan 
});
var problem1view = new app.problemView({ model: problem1 });