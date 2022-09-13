import pandas as pd
from pgmpy.estimators import PC
import matplotlib.pyplot as plt
from matplotlib.patches import ArrowStyle
import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout
import pingouin
from linearmodels.system import SUR


def graph_DAG(edges, 
              data_reg, 
              title = "", 
              fig = False, 
              ax = False, 
              edge_labels = False,
              sig_vals = [0.05, 0.01, 0.001]):
    graph = nx.DiGraph()
    def build_edge_labels(edges, df, sig_vals):
        edge_labels = {}
        for edge in edges:
            controls = [key for key in df.keys() if key not in edge]
            controls = list(set(controls))
            keep_controls = []
            for control in controls:
                control_edges = [ctrl_edge for ctrl_edge in edges if control == ctrl_edge[0] ]
                if (control, edge[1]) in control_edges:
                    keep_controls.append(control)                
#             print(edge, keep_controls)
            pcorr = df.partial_corr(x = edge[0], y = edge[1], covar=keep_controls,
                                  method = "pearson")
            label = str(round(pcorr["r"][0],2))
            pvalue = pcorr["p-val"][0]
#             pcorr = df[[edge[0], edge[1]]+keep_controls].pcorr()
#             label = pcorr[edge[0]].loc[edge[1]]

            for sig_val in sig_vals:
                if pvalue < sig_val: 
                    label = label + "*"   
            
            edge_labels[edge] = label
        return edge_labels
    
    if edge_labels == False:
        edge_labels = build_edge_labels(edges, 
                                        data_reg, 
                                        sig_vals=sig_vals) 
    graph.add_edges_from(edges)
    color_map = ["grey" for g in graph]

    if fig == False and ax == False: fig, ax = plt.subplots(figsize = (20,12))
    graph.nodes()
    plt.tight_layout()
    pos = graphviz_layout(graph)

    edge_labels2 = []
    for u, v, d in graph.edges(data=True):
        if pos[u][0] > pos[v][0]:  
            if (v,u) in edge_labels.keys():
                edge_labels2.append(((u, v,), f'{edge_labels[u,v]}\n\n\n{edge_labels[(v,u)]}'))  
        if (v,u) not in edge_labels.keys():
            edge_labels2.append(((u,v,), f'{edge_labels[(u,v)]}'))
    edge_labels = dict(edge_labels2)

    nx.draw_networkx(graph, pos, node_color=color_map, node_size = 500,
                     with_labels=True,  arrows=True,
                     font_color = "black",
                     font_size = 16, alpha = 1,
                     width = 1, edge_color = "C1",
                     arrowstyle=ArrowStyle("Fancy, head_length=3, head_width=1.5, tail_width=.1"),
                     connectionstyle='arc3, rad = 0.05',
                     ax = ax)
    nx.draw_networkx_edge_labels(graph,
                                 pos,
                                 edge_labels=edge_labels,
                                 font_color='green',
                                 font_size=14,
                                 ax = ax)
# def graph_DAG(edges, 
#               df, 
#               pp, 
#               edge_labels = False, 
#               sig_vals = [.05,.01,.001],
#               title = ""):
#     def build_edge_labels(edges, df, sig_vals):
#         edge_labels = {}
#         for edge in edges:
#             controls = [key for key in df.keys() if key not in edge]
#             controls = list(set(controls))
#             keep_controls = []
#             for control in controls:
#                 control_edges = [ctrl_edge for ctrl_edge in edges if control == ctrl_edge[0] ]
#                 if (control, edge[1]) in control_edges:
#                     keep_controls.append(control)                
#             pcorr = df.partial_corr(x = edge[0], y = edge[1], covar=keep_controls,
#                                   method = "pearson")
#             label = str(round(pcorr["r"][0],2))
#             pvalue = pcorr["p-val"][0]
# #             pcorr = df[[edge[0], edge[1]]+keep_controls].pcorr()
# #             label = pcorr[edge[0]].loc[edge[1]]

#             for sig_val in sig_vals:
#                 if pvalue < sig_val: 
#                     label = label + "*"   
            
#             edge_labels[edge] = label
#         return edge_labels
#     graph = nx.DiGraph()
#     if edge_labels == False:
#         edge_labels = build_edge_labels(edges, 
#                                         df, 
#                                         sig_vals=sig_vals) 
#     graph.add_edges_from(edges)
#     color_map = ["C0" for g in graph]

#     fig, ax = plt.subplots(figsize = (20,20))
#     graph.nodes()
#     plt.tight_layout()
#     pos = graphviz_layout(graph)

#     nx.draw_networkx(graph, pos, node_color=color_map, node_size = 2500,
#                      with_labels=True,  arrows=True,
#                      font_color = "white",
#                      font_size = 26, alpha = 1,
#                      width = 1, edge_color = "C1",
#                      arrowstyle=ArrowStyle("Fancy, head_length=3, head_width=1.5, tail_width=.1"),
#                      connectionstyle='arc3, rad = 0.05',
#                      ax = ax)
    
#     plt.title(title, fontsize = 30)
#     edge_labels2 = []
#     for u, v, d in graph.edges(data=True):
#         if pos[u][0] > pos[v][0]:  
#             if (v,u) in edge_labels.keys():
#                 edge_labels2.append(((u, v,), f'{edge_labels[u,v]}\n\n\n{edge_labels[(v,u)]}'))  
#         if (v,u) not in edge_labels.keys():
#             edge_labels2.append(((u,v,), f'{edge_labels[(u,v)]}'))
#     edge_labels = dict(edge_labels2)

#     nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_color='C2')
    
#     nx.draw_networkx_edge_labels(graph,pos,
#                                  edge_labels=edge_labels,
#                                  font_color='green',
#                                  font_size=20)
#     pp.savefig(fig, bbox_inches = "tight")  
#     plt.show()
#     plt.close()
    
    

def DAG(dag_data, variant, ci_test, sig, return_type = "dag"):
    c = PC(dag_data)
#     edges = c.skeleton_to_pdag(*c.build_skeleton())
    max_cond_vars = len(dag_data.keys()) - 2
    model = c.estimate(return_type = return_type,
                       variant= variant, 
                       significance_level = sig, 
                       max_cond_vars = max_cond_vars, 
                       ci_test = ci_test)
    edges = model.edges()
    
    return edges


def identify_sink_nodes(edges):
    unzipped_edges = list(zip(*edges))
    sink_nodes = unzipped_edges[1]
    caused_causal = {node:[] for node in sink_nodes}
    for source, sink in edges:
        caused_causal[sink].append(source)
    return caused_causal 



def simultaneous_SUR(reg_data, sink_source, model_type = "DAG", constant = True, sig_vals = [0.05, 0.01, 0.001]):
    formulas = {}
    edge_weights = {}
    reg_data.rename(columns={key:key.replace("$\pi$","pi").replace("/","") for key in reg_data.keys()},
                    inplace = True) 
    for variables in sink_source.items():
        sink, source = variables
        sink = sink.replace("$\pi$","pi").replace("/","") 
        formula = sink + " ~"
        i= 0
        for x in source:
            x = x.replace("$\pi$","pi").replace("/","")            
            if i == 0: 
                formula = formula + " " + x
            else:
                formula = formula + " + " + x              
            i=+1

        if constant:formula = formula + "+ Constant"        
        formulas[sink] = formula 
    if constant:
        reg_data["Constant"] = 1
    model = SUR.from_formula(formulas, reg_data)
    results = model.fit(cov_type="unadjusted")
    #save regression results
    SUR_results = pd.DataFrame([results.params, results.pvalues])
    SUR_results.to_excel("SUR" + str(list(reg_data.index)[0])[:10]+"-"+str(list(reg_data.index)[-1])[:10]+".xlsx")
    # print("SUR (formatted endog_exog)", SUR_results, sep = "\n")
#     if constant:
#         reg_data.drop("Constant", axis = 1, inplace = True)
    for ix in results.params.keys():
        if "Constant" not in ix:
            source, sink = ix.split("_")
            sink = sink.replace("CA", "C/A")
            source = source.replace("CA", "C/A")
            edge_weights[(sink,source)] = str(round(results.params[ix],2))
            for sig_val in sig_vals:
                if results.pvalues[ix] < sig_val: 
                    edge_weights[(sink,source)] = edge_weights[(sink,source)] + "*"   
    
    return edge_weights

def DAG_OLS(ols_data, sink_source, filename, ax, diff, dates, constant = True, return_type=""):
    keys = list(ols_data.keys())
    edge_weights = simultaneous_SUR(ols_data, sink_source, constant = constant)
    graph_DAG(edges = list(edge_weights.keys()), 
              data_reg = ols_data,
              edge_labels = edge_weights,
             title = "",
             ax = ax)
    
def DAG_VAR(var_data, sink_source, filename, ax, diff, dates, sig_vals = [0.05, 0.01, 0.001], constant = True, return_type=""):
    reg_dict={}
    edges_weights = {}

    for sink, source in sink_source.items():
        variables = [sink] + source
        for k in range(len(variables)):
            key = variables[k]
            variables.append(key + " Lag")
            if key in sink_source.keys():
                if sink in sink_source[key] and sink not in variables:
                    variables.append(key)
        select_data = var_data[variables]
        select_data.dropna(inplace = True)
        endog_keys = [key for key in variables if "Lag" not in key]
        exog_keys = [key for key in variables if "Lag" in key]
        endog = select_data[endog_keys]
        exog = select_data[exog_keys]
        reg_dict[sink] = VAR(endog, exog, sig_vals, constant = constant)
        pd.DataFrame(reg_dict[sink])
        for sce in source:
            edges_weights[(sce, sink)] = reg_dict[sink][sink][sce+ " Lag"]
    graph_DAG(edges = list(edges_weights.keys()), 
              data_reg = select_data,
              edge_labels = edges_weights,
             ax= ax,
             title = "") 
    for sink, dct in reg_dict.items():
        # print("VAR: estimated endog = " + sink, pd.DataFrame(dct), "", sep = "\n")
        
        lag_keys = [key + " Lag" for key in dct] 
        if "Constant" in dct: lag_keys = lag_keys + ["Constant"]
        excel_df = pd.DataFrame(dct).T[lag_keys].T #["r2"]
        fname = sink + filename  
        excel_df.to_excel(fname.replace("/","").replace("\\","")+".xlsx")


def VAR(endog, exog, sig_vals = [0.05, 0.01, 0.001], constant = True):
    
    if constant:
        exog["Constant"] = 1
    endog_keys= list(endog.keys())
    exog_keys = list(exog.keys())    
    model = SUR.multivariate_ls(endog,exog)
    results = model.fit()
    
    # save results with columns defined by endogenous variables
    index = results.pvalues.index.str.split("_")
    df = pd.DataFrame(index.to_list(), columns = ["Sink", "Source"])
    df["Coef"] = results.params.values
    df["tstats"]=results.tstats.values
    df["pvalues"]=results.pvalues.values
    results =df.pivot(columns = "Sink", index = "Source")
    results = results.round(3)
    keys1 = list(results["Coef"].keys())
    params = results["Coef"].astype(str)
    for endog in keys1:
        keys2 = list(params[endog].keys())
        for sig_val in sig_vals:
            bool_index = results["pvalues"][endog]<sig_val
            bool_slice = params[endog][bool_index]
            params[endog][bool_index] = params[endog][bool_index].str.cat(["*"]*len(bool_slice), sep = "")#.str.cat("*"))

    return params

