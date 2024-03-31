#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  5 23:28:03 2022

@author: hill103

this script stores utils functions
"""



import os
import numpy as np
import pandas as pd
from config import print, output_path
#import scanpy as sc
#sc.settings.verbosity = 0  # verbosity: errors (0), warnings (1), info (2), hints (3)



def calcRMSE(truth, predicted):
    '''
    calculate RMSE

    Parameters
    ----------
    truth : 1-D numpy array
        true values.
    predicted : 1-D numpy array
        predictions.

    Returns
    -------
    float
        RMSE
    '''

    return np.sqrt(((predicted - truth) ** 2).mean())



def reportRMSE(true_theta, pred_theta):
    '''
    calculate the RMSE of theta (celltype proportion) across all spots
    
    we first calculate the RMSE of each spot, then calculate the MEAN of RMSE values across all spots

    Parameters
    ----------
    true_theta : 2-D numpy array (spots * celltypes)
        true values.
    pred_theta : 2-D numpy array (spots * celltypes)
        predictions.

    Returns
    -------
    float
        RMSE across all spots
    '''
    
    return np.array([calcRMSE(true_theta[i,], pred_theta[i,]) for i in range(true_theta.shape[0])]).mean()



def reparameterTheta(theta, e_alpha):
    '''
    re-parametrization w = e^alpha * theta

    Parameters
    ----------
    theta : 3-D numpy array (#spot * #celltype * 1)
        theta (celltype proportion).
    e_alpha : 1-D numpy array
        e^alpha (spot-specific effect).

    Returns
    -------
    w : 3-D numpy array (#spot * #celltype * 1)
        re-parametrization w = e^alpha * theta.

    '''
    
    return e_alpha[:, None, None] * theta



def read_spatial_data(spatial_file):
    '''
    read spatial data saved as a CSV file by Scanpy

    Parameters
    ----------
    spatial_file : string
        full path of input csv file of raw nUMI counts in spatial transcriptomic data (spots * genes).
        
    Returns
    -------
    a AnnData object
    '''
    
    # Read spatial spot-level data
    spatial_spot_obj = sc.read_csv(spatial_file)
    spatial_spot_obj.layers['raw_nUMI'] = spatial_spot_obj.X.copy()
    print(f'read spatial data from file {spatial_file}')
    print(f'total {spatial_spot_obj.n_obs} spots; {spatial_spot_obj.n_vars} genes\n')
    
    # check whether cell name and gene name are unique
    if len(set(spatial_spot_obj.obs_names.tolist())) < spatial_spot_obj.n_obs:
        raise Exception('spot barcodes in spatial data are not unique!')
        
    if len(set(spatial_spot_obj.var_names.tolist())) < spatial_spot_obj.n_vars:
        raise Exception('gene names in spatial data are not unique!')
    
    # Normalize each cell by total counts over ALL genes
    sc.pp.normalize_total(spatial_spot_obj, target_sum=1, inplace=True)
    
    return spatial_spot_obj



def read_scRNA_data(ref_file, ref_anno_file):
    '''
    read scRNA-seq data saved as a CSV file by Scanpy, also read cell-type annotation, then subset cells with cell-type annotation

    Parameters
    ----------
    ref_file : string
        full path of input csv file of raw nUMI counts in scRNA-seq data (cells * genes).
    ref_anno_file : string
        full path of input csv file of cell-type annotations for all cells in scRNA-seq data.
        
    Returns
    -------
    a AnnData object
    '''
    
    # Read scRNA cell-level data and cell-type annotation
    scrna_obj = sc.read_csv(ref_file)
    print(f'read scRNA-seq data from file {ref_file}')
    print(f'total {scrna_obj.n_obs} cells; {scrna_obj.n_vars} genes')
    
    # check whether cell name and gene name are unique
    if len(set(scrna_obj.obs_names.tolist())) < scrna_obj.n_obs:
        raise Exception('spot barcodes in spatial data are not unique!')
        
    if len(set(scrna_obj.var_names.tolist())) < scrna_obj.n_vars:
        raise Exception('gene names in spatial data are not unique!')

    scrna_celltype = pd.read_csv(ref_anno_file, index_col=0)
    print(f'read scRNA-seq cell-type annotation from file {ref_anno_file}')
    print(f'total {len(set(scrna_celltype.iloc[:,0]))} cell-types')
    
    # check whether cell name are unique
    if len(set(scrna_celltype.index.to_list())) < scrna_celltype.shape[0]:
        raise Exception('cell barcodes in scRNA-seq cell-type annotation are not unique!')
        
    # check overlap of cells in gene expression and cell-type annotation
    overlap_cells = sorted(list(set(scrna_celltype.index.to_list()) & set(scrna_obj.obs_names)))
    if len(overlap_cells) < scrna_celltype.shape[0]:
        print(f'WARNING: {scrna_celltype.shape[0]-len(overlap_cells)} cells in cell-type annotation but not found in nUMI matrix')
    
    # only keep cells with cell-type annotations
    scrna_obj = scrna_obj[overlap_cells, ].copy()
    assert((scrna_obj.obs_names == overlap_cells).all())
    print(f'subset cells with cell-type annotation, finally keep {scrna_obj.n_obs} cells; {scrna_obj.n_vars} genes\n')

    # add cell-type annotation to metadata
    scrna_celltype = scrna_celltype.loc[overlap_cells, :]
    assert((scrna_obj.obs_names == scrna_celltype.index).all())
    scrna_obj.obs['celltype'] = pd.Categorical(scrna_celltype.iloc[:,0])  # Categoricals are preferred for efficiency
    # make a DEEP COPY of raw nUMI count
    scrna_obj.layers['raw_nUMI'] = scrna_obj.X.copy()
    # Normalize each cell by total counts over ALL genes
    sc.pp.normalize_total(scrna_obj, target_sum=1, inplace=True)
    
    return scrna_obj



def run_DE(sc_obj, n_marker_per_cmp, use_fdr, p_val_cutoff, fc_cutoff, pct1_cutoff, pct2_cutoff, sortby_fc, save_result=False, save_file_name=None):
    '''
    differential on cell-types in scRNA-seq data.
    
    we compare each cell-type with another one cell-type at a time.
    
    only choose TOP X marker genes for one comparison with one cell-type vs another one cell-type, with filtering (the FDR adjusted p value <= 0.05 + fold change >= 1.2 + pct.1 >= 0.8 + pct.2 <= 0.2, and sorting by fold change (by default). Then combine all marker genes from all comparisons.
    
    Note: the genes in object are overlapped genes with spatial data only.
    
    cell-type annotation is saved in object metadata <celltype>
    
    gene expression in AnnData object has already been normalized by sequencing depth

    Parameters
    ----------
    sc_obj : AnnData object
        scRNA-seq data object.
    n_marker_per_cmp : int
        number of TOP marker genes for each comparison in DE
    use_fdr : bool
        whether to use FDR adjusted p value for filtering and sorting
    p_val_cutoff : float
        threshold of p value (or FDR if --use_fdr is true) in marker genes filtering
    fc_cutoff : float
        threshold of fold change (without log transform!) in marker genes filtering
    pct1_cutoff : float
        threshold of pct.1 in marker genes filtering
    pct2_cutoff : float
        threshold of pct.2 in marker genes filtering
    sortby_fc : bool
        whether to sort marker genes by fold change
    save_result : bool
        if true, save dataframe of DE result to csv file
    save_file_name : string
        file name (without path) for saving DE result
        
    Returns
    -------
    marker_gene_list : list
        identified cell-type specific marker gene list
    '''
    
    def calc_pct(sc_obj, celltype):
        '''
        calculate pct of genes expressed in cells within one celltype.
        
        raw nUMI count saved in layer <raw_nUMI>

        Parameters
        ----------
        sc_obj : AnnData object
            scRNA-seq data object.
        celltype : string
            name of one cell-type.

        Returns
        -------
        pct_df : Series with genes as index
            A Series including genes and corresponding pcts.
        '''
        
        sub_obj = sc_obj[sc_obj.obs['celltype'] == celltype]
        # get raw nUMI count (cells * genes)
        sub_df = sc.get.obs_df(sub_obj, layer='raw_nUMI', keys=sub_obj.var_names.to_list())
        assert sub_df.shape[0] > 0, f'Error! there is no cell for cell-type `{celltype}`'
        # column sum divided by number of rows
        return ((sub_df>0).sum(axis=0)) / (sub_df.shape[0])
        
        
    
    print('Differential analysis across cell-types on scRNA-seq data...')
    celltypes = sorted(list(set(sc_obj.obs['celltype'])))
    
    scrna_marker_genes = list()
    de_result_list = []
    
    if use_fdr:
        pval_col = 'pvals_adj'
    else:
        pval_col = 'pvals'
    
    # first calculate pct for each cell-type
    pct_dict = {}
    for this_celltype in celltypes:
        pct_dict[this_celltype] = calc_pct(sc_obj, this_celltype)
    
    # perform test
    for this_celltype in celltypes:
        
        for other_celltype in celltypes:
            if this_celltype == other_celltype:
                continue
            
            # compare one cell-type against another cell-type
            sc.tl.rank_genes_groups(sc_obj, groupby='celltype', use_raw=False, corr_method='benjamini-hochberg',
                                    method='wilcoxon', groups=[this_celltype], reference=other_celltype)
            tmp_df = sc.get.rank_genes_groups_df(sc_obj, group=None)
            
            # add pcts
            tmp_df = tmp_df.merge(pct_dict[this_celltype].rename('pct1'), left_on='names', right_index=True, validate='one_to_one')
            tmp_df = tmp_df.merge(pct_dict[other_celltype].rename('pct2'), left_on='names', right_index=True, validate='one_to_one')
            
            # filter genes
            tmp_df = tmp_df.loc[(tmp_df[pval_col]<=p_val_cutoff) & (tmp_df['logfoldchanges']>=np.log2(fc_cutoff)) & (tmp_df['pct1']>=pct1_cutoff) & (tmp_df['pct2']<=pct2_cutoff)]
            
            # add cell-types
            tmp_df['celltype1'] = this_celltype
            tmp_df['celltype2'] = other_celltype
            
            if tmp_df.shape[0] <= n_marker_per_cmp:
                
                if tmp_df.shape[0] < n_marker_per_cmp:
                    print(f'WARNING: only {tmp_df.shape[0]} genes passing filtering (<{n_marker_per_cmp}) for {this_celltype} vs {other_celltype}')
                
                # no need to further rank, directly select all available genes
                scrna_marker_genes += tmp_df['names'].to_list()
                
                # combine DE result
                tmp_df['selected'] = 1
            
            else:
                '''
                # rank of pct.1/pct.2
                tmp_df['pct_divide'] = tmp_df['pct1'] / tmp_df['pct2']
                tmp_df.sort_values(by='pct_divide', ascending=False, inplace=True)
                tmp_df['pct_rank'] = range(tmp_df.shape[0])
                
                # rank of log fold change
                tmp_df.sort_values(by='logfoldchanges', ascending=False, inplace=True)
                tmp_df['logfc_rank'] = range(tmp_df.shape[0])
                
                tmp_df['comb_rank'] = tmp_df['pct_rank'] + tmp_df['logfc_rank']
                tmp_df.sort_values(by=['comb_rank', 'logfoldchanges'], ascending=[True, False], inplace=True)
                '''
                
                # sort by fold change or p value
                if sortby_fc:
                    tmp_df.sort_values(by=[pval_col, 'logfoldchanges'], ascending=[True, False], inplace=True)
                else:
                    tmp_df.sort_values(by=['logfoldchanges', pval_col], ascending=[False, True], inplace=True)
                
                # select top X marker genes
                scrna_marker_genes += tmp_df['names'].to_list()[:n_marker_per_cmp]
                # combine DE result
                tmp_df['selected'] = 0
                tmp_df.loc[tmp_df.index.to_list()[:n_marker_per_cmp], 'selected'] = 1
            
            tmp_df.rename(columns={'names': 'gene'}, inplace=True)
            de_result_list.append(tmp_df.loc[:, ['gene', 'logfoldchanges', 'pvals', 'pvals_adj', 'pct1', 'pct2', 'celltype1', 'celltype2', 'selected']].copy())

    scrna_marker_genes = sorted(list(set(scrna_marker_genes)))
    print(f'finally selected {len(scrna_marker_genes)} cell-type marker genes\n')
    
    if save_result:
        pd.concat(de_result_list).to_csv(os.path.join(output_path, save_file_name), index=False)
    
    return scrna_marker_genes



def run_DE_only(ref_file, ref_anno_file, spatial_genes, n_marker_per_cmp, use_fdr, p_val_cutoff, fc_cutoff, pct1_cutoff, pct2_cutoff, sortby_fc, save_result=False):
    '''
    read scRNA-seq raw nUMI and cell-type annotation, then perform DE analysis.
    
    Note: the genes in scRNA-seq data need to be subsetted to overlapped genes with spatial data only.

    Parameters
    ----------
    ref_file : string
        full path of input csv file of raw nUMI counts in scRNA-seq data (cells * genes).
    ref_anno_file : string
        full path of input csv file of cell-type annotations for all cells in scRNA-seq data.
    spatial_genes : list
        genes included in spatial dataset.
    n_marker_per_cmp : int
        number of TOP marker genes for each comparison in DE
    use_fdr : bool
        whether to use FDR adjusted p value for filtering and sorting
    p_val_cutoff : float
        threshold of p value (or FDR if --use_fdr is true) in marker genes filtering
    fc_cutoff : float
        threshold of fold change (without log transform!) in marker genes filtering
    pct1_cutoff : float
        threshold of pct.1 in marker genes filtering
    pct2_cutoff : float
        threshold of pct.2 in marker genes filtering
    sortby_fc : bool
        whether to sort marker genes by fold change
    save_result : bool
        if true, save dataframe of DE result to csv file
        
    Returns
    -------
    marker_gene_profile : DataFrame
        average gene expressions of identified cell-type specific marker genes from refer scRNA-seq data
    '''
    
    scrna_obj = read_scRNA_data(ref_file, ref_anno_file)
    
    # subset genes
    overlap_genes = list(set(spatial_genes).intersection(set(scrna_obj.var_names)))
    #if len(overlap_genes) < len(spatial_genes):
        #print(f'{len(spatial_genes)-len(overlap_genes)} genes in spatial data but not found in scRNA-seq data: {", ".join(set(spatial_genes).difference(set(overlap_genes)))}\n')
    
    scrna_obj = scrna_obj[:, overlap_genes].copy()
    
    # DE
    marker_genes = run_DE(scrna_obj, n_marker_per_cmp, use_fdr, p_val_cutoff, fc_cutoff, pct1_cutoff, pct2_cutoff, sortby_fc, save_result, 'DE celltype markers.csv')
    
    # generate average gene expressions (gene signature) for cell-types based on normalized values
    tmp_df = sc.get.obs_df(scrna_obj, keys=marker_genes)
    
    tmp_df['celltype'] = scrna_obj.obs['celltype']

    tmp_df = tmp_df.groupby(['celltype']).mean()
    
    return tmp_df



def rerun_DE(scRNA_df, scRNA_celltype, n_marker_per_cmp, use_fdr, p_val_cutoff, fc_cutoff, pct1_cutoff, pct2_cutoff, sortby_fc, save_result=False):
    '''
    rerun DE on CVAE transformed scRNA-seq data
    
    genes are only overlapped genes between spatial and scRNA-seq data
    
    gene expression values are already normalized by sequencing depth

    Parameters
    ----------
    scRNA_df : dataframe
        normalized gene expression after CVAE tranforming on scRNA-seq data (cells * genes).
    scRNA_celltype : dataframe
        cell-type annotations for cells in scRNA-seq data. Only 1 column named <celltype>
    n_marker_per_cmp : int
        number of TOP marker genes for each comparison in DE
    use_fdr : bool
        whether to use FDR adjusted p value for filtering and sorting
    p_val_cutoff : float
        threshold of p value (or FDR if --use_fdr is true) in marker genes filtering
    fc_cutoff : float
        threshold of fold change (without log transform!) in marker genes filtering
    pct1_cutoff : float
        threshold of pct.1 in marker genes filtering
    pct2_cutoff : float
        threshold of pct.2 in marker genes filtering
    sortby_fc : bool
        whether to sort marker genes by fold change
    save_result : bool
        if true, save dataframe of DE result to csv file
        
    Returns
    -------
    marker_gene_list : list
        a list of cell-type specific marker genes based on DE on CVAE tranformed gene expressions.
    '''
    
    # first build a AnnData object and replace the normalized data with CVAE transformed gene expressions
    scrna_obj = sc.AnnData(scRNA_df)
    # make a DEEP COPY of raw nUMI count, though it's actually normalized values
    scrna_obj.layers['raw_nUMI'] = scrna_obj.X.copy()
    
    assert((scrna_obj.obs_names == scRNA_celltype.index).all())
    # add cell-type annotation to metadata
    scrna_obj.obs['celltype'] = pd.Categorical(scRNA_celltype.iloc[:,0])  # Categoricals are preferred for efficiency
    
    # do not normalize by sequencing depth as it's already normalized
    # so directly run DE on values in AnnData.X
    return run_DE(scrna_obj, n_marker_per_cmp, use_fdr, p_val_cutoff, fc_cutoff, pct1_cutoff, pct2_cutoff, sortby_fc, save_result, 'redo DE celltype markers.csv')



# check total size of a Python object such as a Dictionary
# ref https://code.activestate.com/recipes/577504/
def total_size(o, handlers={}, verbose=False):
    """ Returns the approximate memory footprint an object and all of its contents.

    Automatically finds the contents of the following builtin containers and
    their subclasses:  tuple, list, deque, dict, set and frozenset.
    To search other containers, add handlers to iterate over their contents:

        handlers = {SomeContainerClass: iter,
                    OtherContainerClass: OtherContainerClass.get_elements}

    """
    
    from sys import getsizeof, stderr
    from itertools import chain
    from collections import deque
    try:
        from reprlib import repr
    except ImportError:
        pass
    
    dict_handler = lambda d: chain.from_iterable(d.items())
    all_handlers = {tuple: iter,
                    list: iter,
                    deque: iter,
                    dict: dict_handler,
                    set: iter,
                    frozenset: iter,
                    }
    all_handlers.update(handlers)     # user handlers take precedence
    seen = set()                      # track which object id's have already been seen
    default_size = getsizeof(0)       # estimate sizeof object without __sizeof__

    def sizeof(o):
        if id(o) in seen:       # do not double count the same object
            return 0
        seen.add(id(o))
        s = getsizeof(o, default_size)

        if verbose:
            print(s, type(o), repr(o), file=stderr)

        for typ, handler in all_handlers.items():
            if isinstance(o, typ):
                s += sum(map(sizeof, handler(o)))
                break
        return s

    return sizeof(o)



def check_decoder(cvae, decoder, data, labels):
    '''
    since we first create a decoder then update its weights based on the corresponding weights in CVAE, we need to double check the weights are updated correctly, and the decoded output matchs the CVAE output

    Parameters
    ----------
    cvae : Keras model
        already trained CVAE model
    decoder : Keras model
        a separated decoder whose weights are already updated, i.e. it should give the same decoded output with CVAE
    data : 2-D numpy array
        data used for checking decoder (columns are genes, rows are cells, spatial spots or pseudo-spots)
    labels : 1-D numpy array
        corresponding conditional variables for each row in data

    Returns
    -------
    None.
    '''
    
    from tensorflow.keras.models import Model
    
    # a tmp model to get the embedding after sampling and decoder output at the same time
    tmp_model = Model([cvae.get_layer('encoder_input').input, cvae.get_layer('cond_input').input],
                      [cvae.get_layer('z').output, cvae.get_layer('decoder_output_act').output],
                      name='tmp_model')
    # the preditions of embedding and decoder output
    [tmp_embedding, tmp_output] = tmp_model.predict([data, labels])
    # feed the embedding to the new decoder
    tmp_output2 = decoder.predict([tmp_embedding, labels])
    # are them the same?
    tmp = np.all((tmp_output-tmp_output2)<1e-12)
    assert(tmp==True)
    
    
    
def diagnosisCVAE(cvae, encoder, decoder, spatial_df, spatial_embed, spatial_transformed_df, scRNA_df, scRNA_celltype, celltypes, celltype_count_dict, scRNA_embed, n_spot, pseudo_spots_df, pseudo_spots_celltype, n_cell_in_spot, scRNA_min_max_scaler, scRNA_decode_df, scRNA_decode_avg_df, new_markers):
    '''
    save CVAE related Keras models to h5 file, generate figures to diagnosis the training of CVAE

    Parameters
    ----------
    cvae : Keras model
        already trained CVAE model
    encoder: Keras model
        encoder part extract from CVAE model
    decoder : Keras model
        a separated decoder whose weights are already updated, i.e. it should give the same decoded output with CVAE
    spatial_df : dataframe
        normalized gene expression in spatial transcriptomic data (spots * genes).
    spatial_embed : 2-D numpy array
        mu in latent space of spatial spots (spots * latent neurons)
    spatial_transformed_df : dataframe
        CVAE transformed (platform effect adjusted) spatial spot gene raw nUMI counts (spots * genes)
    scRNA_df : dataframe
        normalized gene expression in scRNA-seq data (cells * genes).
    scRNA_celltype : dataframe
        cell-type annotations for cells in scRNA-seq data. Only 1 column named <celltype>
    celltypes : list
        already sorted unique cell-types. Its order matters, and will be the order in pseudo_spots_celltype (columns) and cell-type gene expression profile (rows)
    celltype_count_dict : dict
        number of cells in reference scRNA-seq data for each cell-type
    scRNA_embed : 2-D numpy array
        mu in latent space of scRNA-seq cells (cells * latent neurons)
    n_spot : int
        total number of generated pseudo-spots (including training and validation pseudo-spots, NOT include scRNA-seq cells)
    pseudo_spots_df : dataframe
        pseudo-spot gene expression (pseudo-spots * genes; including scRNA-seq cells at the end). The mu in latent space will be calculated inside this function
    pseudo_spots_celltype : dataframe
        pseudo-spot cell-type proportions (pseudo-spots * cell-types; including scRNA-seq cells at the end)
    n_cell_in_spot : list
        number of cells in pseudo-spots (including scRNA-seq cells at the end)
    scRNA_min_max_scaler : sklearn MinMaxScaler object
        scaler of CVAE training data (training pseudo-spots + scRNA-seq cells)
    scRNA_decode_df : dataframe
        CVAE decodered gene expression (normalized) of scRNA-seq cells (cells * genes)
    scRNA_decode_avg_df : dataframe
        CVAE decodered average gene expression (normalized) of cell-types in scRNA-seq data (cell-types * genes)
    new_markers : list or None
        marker genes from re-run DE on CVAE transformed scRNA-seq data. It will be None if not re-run DE (rerun_DE=False)
        
    Returns
    -------
    None.

    '''
    
    from tensorflow.keras.utils import plot_model
    
    print('\nsave variables related to CVAE to files!')
    
    plot_model(cvae, to_file=os.path.join(output_path, 'CVAE model.png'), show_shapes=True)
    
    spatial_transformed_df.to_csv(os.path.join(output_path, 'spatial_spots_transformToscRNA_decoded.csv'))
    scRNA_decode_avg_df.to_csv(os.path.join(output_path, 'scRNA_decoded_avg_exp_bycelltypes.csv'))
    cvae.save(os.path.join(output_path, 'CVAE_whole.h5'))
    encoder.save(os.path.join(output_path, 'CVAE_encoder.h5'))
    decoder.save(os.path.join(output_path, 'CVAE_decoder.h5'))
    
    
    # plot variance of mu of spatial spots and scRNA-seq cells
    import matplotlib
    import matplotlib.pyplot as plt
    import seaborn as sns
    sns.set()
    
    latent_var = np.concatenate((spatial_embed, scRNA_embed), axis=0).var(axis=0)
    plt.figure()
    ax = sns.histplot(x=np.log10(latent_var))
    ax.set(xlabel='log10(var(mu))')
    plt.savefig(os.path.join(output_path, 'histogram of variance of latent neurons on spatial spots and scRNA-seq cells.png'))
    plt.close()
    
    
    # plot histogram of transformed spots nUMI sum
    plt.figure()
    ax = sns.histplot(x=np.sum(spatial_transformed_df.values, axis=1))
    ax.set(xlabel='Sum of nUMI per spatial spot after transformation')
    plt.savefig(os.path.join(output_path, 'histogram of sum of nUMI of spatial spots after transformation.png'))
    plt.close()
    
    
    # plot zero percentage of marker genes in spatial spots after transformation
    plt.figure()
    if new_markers is None:
        tmp_mtx = spatial_transformed_df.values
    else:
        tmp_mtx = spatial_transformed_df.loc[:, new_markers].values
    ax = sns.histplot(x=np.sum(tmp_mtx==0, axis=1)/tmp_mtx.shape[1])
    ax.set(xlabel=f'Zero percentage of {tmp_mtx.shape[1]} genes per spot after transformation')
    ax.set_xlim(xmin=0, xmax=1)
    plt.savefig(os.path.join(output_path, 'histogram of zero percentage of spatial spots after transformation.png'))
    plt.close()
    
    
    # plot umap of latent space of spatial spots and scRNA-seq cells plus pseudo spots
    import umap
    from distinctipy import distinctipy
    
    # embed of decoded average marker gene expression
    marker_embed = encoder.predict([scRNA_min_max_scaler.transform(scRNA_decode_df), np.full((scRNA_decode_df.shape[0],1), 0)])[0]
    
    pseudo_spot_embed = encoder.predict([scRNA_min_max_scaler.transform(pseudo_spots_df.iloc[:n_spot, :]), np.full((n_spot,1), 0)])[0]
    
    # the order will affect the point overlay, first row draw first
    # umap has embeded seed (default 42), by specify random_state, umap will use special mode to keep reproducibility
    all_umap = umap.UMAP(random_state=42).fit_transform(np.concatenate((pseudo_spot_embed, scRNA_embed, marker_embed, spatial_embed), axis=0))
    
    # add cell/spot count in the annotation
    plot_df = pd.DataFrame({'UMAP1': all_umap[:, 0],
                            'UMAP2': all_umap[:, 1],
                            'celltype': ['pseudo']*n_spot + [f'{x} ({celltype_count_dict[x]})' for x in scRNA_celltype.celltype.to_list()] + [f'{x} ({celltype_count_dict[x]})' for x in scRNA_decode_df.index.to_list()] + [f'spatial ({spatial_df.shape[0]})']*spatial_df.shape[0],
                            'dot_type': ['pseudo spot']*n_spot + ['cell']*scRNA_df.shape[0] + ['marker']*scRNA_decode_df.shape[0] + ['spatial spot']*spatial_df.shape[0],
                            'dataset': ['scRNA-seq']*(scRNA_df.shape[0]+scRNA_decode_df.shape[0]+n_spot) + ['spatial']*spatial_df.shape[0]
                            },
                           index = [f'pseudo{x}' for x in range(n_spot)] + scRNA_df.index.to_list() + [f'{x}-marker' for x in scRNA_decode_df.index.to_list()] + spatial_df.index.to_list())
    
    plot_sizes = {'cell': 20, 'spatial spot': 20, 'marker': 200, 'pseudo spot': 20}
    plot_markers = {'cell': 'o', 'spatial spot': 'o', 'marker': 'X', 'pseudo spot': 'o'}
    plot_colors = {}
    for one_celltype, one_color in zip([f'spatial ({spatial_df.shape[0]})']+[f'{x} ({celltype_count_dict[x]})' for x in celltypes], distinctipy.get_colors(n_celltype+1)):
        plot_colors[one_celltype] = one_color
    # assign pseudo spots as gray80
    plot_colors['pseudo'] = '#cccccc'
    
    #plt.figure(figsize=(6.4*2*2, 4.8*2))
    sns.set_style("darkgrid")
    
    # relplot return a FacetGrid object
    # specify figure size by Height (in inches) of each facet, and Aspect ratio of each facet
    fgrid = sns.relplot(data=plot_df, x='UMAP1', y='UMAP2', hue='celltype', size='dot_type', style='dot_type', sizes=plot_sizes, markers=plot_markers, palette=plot_colors, kind='scatter', col='dataset', col_order=['scRNA-seq', 'spatial'], height=4.8*2, aspect=6.4/4.8)
    fgrid.set(xlabel='Embedding Dimension 1', ylabel='Embedding Dimension 2')
    # Put the legend out of the figure
    #ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    
    # add cell-type annotations around marker coordinates
    # adjustText do not support seaborn relplot
    #from adjustText import adjust_text
    # fgrid.axes return an array of all axes in the figure
    ax = fgrid.axes[0, 0]
    texts = []
    sub_plot_df = plot_df.loc[plot_df['dot_type']=='marker']
    for one_row in sub_plot_df.index:
        texts.append(ax.text(sub_plot_df.at[one_row, 'UMAP1'], sub_plot_df.at[one_row, 'UMAP2'], sub_plot_df.at[one_row, 'celltype'].split(' (')[0], weight='bold'))
    #adjust_text(texts)
    plt.savefig(os.path.join(output_path, 'UMAP of spatial spots and scRNA-seq cells with markers.png'))
    plt.close()
    
    
    # plot distribution of number of cells in pseudo-spots
    # first n_spot + #scRNA-seq cells of the records are just the pseudo-spots + scRNA-seq data, with the row order matches
    tmp_df = plot_df.iloc[:(n_spot+scRNA_df.shape[0]), :]
    tmp_df = tmp_df.assign(n_cell_in_spot = n_cell_in_spot)
 
    # generate a colormap with a specified color for NA (spatial spots), but not work for relplot...
    #my_cmap = sns.color_palette("viridis", as_cmap=True)
    #my_cmap.set_bad(color=plot_colors[f'spatial ({spatial_df.shape[0]})'])
    
    # show the full legend of colorbar in relplot, otherwise it will only show a sample of evenly spaced values (The FacetGrid hue is categorical, not continuous)
    #fgrid = sns.relplot(data=tmp_df, x='UMAP1', y='UMAP2', hue='#cell_in_spot', palette='viridis', kind='scatter', col='dataset', col_order=['scRNA-seq', 'spatial'], height=4.8*2, aspect=6.4/4.8, legend='full')
    #fgrid.set(xlabel='Embedding Dimension 1', ylabel='Embedding Dimension 2')
    
    # instead use plt.subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, sharey=True, sharex=True, figsize=(6.4*4, 4.8*2))
    # left panel: scatter plot of pseudo-spots
    sc = ax1.scatter(tmp_df['UMAP1'], tmp_df['UMAP2'], c=tmp_df['n_cell_in_spot'], cmap='cubehelix', s=10, marker='o')
    ax1.set_title('dataset = scRNA-seq')
    ax1.set_xlabel('Embedding Dimension 1')
    ax1.set_ylabel('Embedding Dimension 2')
    
    # right panel: scatter plot of spatial spots
    tmp_df = plot_df.loc[plot_df['dot_type']=='spatial spot', :]
    ax2.scatter(tmp_df['UMAP1'], tmp_df['UMAP2'], color=plot_colors[f'spatial ({spatial_df.shape[0]})'], s=10, marker='o')
    ax2.set_title('dataset = spatial')
    ax2.set_xlabel('Embedding Dimension 1')
    ax2.set_ylabel('Embedding Dimension 2')
    
    # add colorbar with title to the most right (https://stackoverflow.com/questions/13784201/how-to-have-one-colorbar-for-all-subplots, conflict with tight_layout)
    cbar = fig.colorbar(sc, ax=ax2)
    cbar.ax.set_title('#cell in spot')
    
    fig.tight_layout()
    fig.savefig(os.path.join(output_path, 'distribution of number of cells in pseudo-spots.png'))
    plt.close()
    
    
    # plot distribution of cell-type proportions of each cell-type
    # tried to use PDF format, but encountered error TeX capacity exceeded, since too many dots in figure
    for this_celltype in celltypes:
        # first n_spot + #scRNA-seq cells of the records are just the pseudo-spots + scRNA-seq data, with the row order matches
        tmp_df = plot_df.iloc[:(n_spot+scRNA_df.shape[0]), :]
        # don't forget the .values
        tmp_df = tmp_df.assign(proportion = pseudo_spots_celltype[this_celltype].values)
        
        # start to plot
        fig, axes = plt.subplots(1, 2, sharey=True, sharex=True, figsize=(6.4*4, 4.8*2))
        (ax1, ax2) = axes.flat
        # left panel: scatter plot of pseudo-spots
        sc = ax1.scatter(tmp_df['UMAP1'], tmp_df['UMAP2'], c=tmp_df['proportion'], cmap='cubehelix', s=10, marker='o', norm=matplotlib.colors.Normalize(vmin=0, vmax=1))
        # plot marker gene profiles with different marker also color (same color is hard to recognize the cross)
        ax1.scatter(plot_df.at[f'{this_celltype}-marker', 'UMAP1'], plot_df.at[f'{this_celltype}-marker', 'UMAP2'], color='red', s=120, marker='X')
        ax1.set_title('dataset = scRNA-seq')
        ax1.set_xlabel('Embedding Dimension 1')
        ax1.set_ylabel('Embedding Dimension 2')
        
        # right panel: scatter plot of spatial spots
        # interpolate the grid for contour plot
        from scipy.interpolate import griddata
        grid_x, grid_y = np.mgrid[tmp_df['UMAP1'].min():tmp_df['UMAP1'].max():0.025, tmp_df['UMAP2'].min():tmp_df['UMAP2'].max():0.025]
        grid_z = griddata(tmp_df.loc[:, ['UMAP1', 'UMAP2']].values, tmp_df['proportion'].values, (grid_x, grid_y), method='linear',  fill_value=np.nan)
        
        try:
            ax2.contourf(grid_x, grid_y, grid_z, cmap='cubehelix', norm=matplotlib.colors.Normalize(vmin=0, vmax=1), alpha=0.3)
        except:
            pass
        
        tmp_df2 = plot_df.loc[plot_df['dot_type']=='spatial spot', :]
        ax2.scatter(tmp_df2['UMAP1'], tmp_df2['UMAP2'], color=plot_colors[f'spatial ({spatial_df.shape[0]})'], s=10, marker='o')
        ax2.set_title('dataset = spatial')
        ax2.set_xlabel('Embedding Dimension 1')
        ax2.set_ylabel('Embedding Dimension 2')
        
        # add colorbar with title
        cbar = fig.colorbar(sc, ax=ax2)
        cbar.ax.set_title('proportion')
        
        fig.suptitle(this_celltype)
        
        fig.tight_layout()
        
        # make sure the file name is valid
        fig.savefig(os.path.join(output_path, f'distribution of {"".join(x for x in this_celltype if (x.isalnum() or x in "._- "))} proportions.png'))
        plt.close()
    
    
    # save spatial spot UMAP coordinates
    plot_df.loc[plot_df['dot_type']=='spatial spot', ['UMAP1', 'UMAP2']].to_csv(os.path.join(output_path, 'spatial spots UMAP coordinates.csv'))
    # save scRNA-seq cells UMAP coordinates
    plot_df.loc[plot_df['dot_type']=='cell', ['UMAP1', 'UMAP2']].to_csv(os.path.join(output_path, 'scRNA-seq cells UMAP coordinates.csv'))
    
    
    
def plot_imputation(df, grid_df, contours, hierarchy, figname, figsize=(6.4, 4.8)):
    '''
    draw scatter plot of spatial spots and imputed spots for diagnosis.

    Parameters
    ----------
    df : dataframe
        dataframe of spatial spots at original resolution, with columns 'x', 'y', 'border'.
    grid_df : dataframe
        dataframe of generated grid points at higher resolution, with columns 'x', 'y'.
    contours : tuple
        contours variable returned by cv2.findContours, used for creating grid.
    hierarchy : 3-D numpy array (1 * #contours * 4)
        hierarchy variable returned by cv2.findContours, used for creating grid.
    figname: string
        name of figure.
    figsize : tuple, optional
        figure size. The default is (6.4, 4.8).

    Returns
    -------
    None.
    '''
    
    import matplotlib.pyplot as plt
    import seaborn as sns
    sns.set_theme()
    
    plt.figure(figsize=figsize)
    
    # scatter plot of original spatial spots, highlighting edge spots
    sns.scatterplot(data=df, x='x', y='y', hue='border', s=100, alpha=0.5, legend=False)
    
    outer_edges = [] # each element is a single outer edge with several points
    inner_edges = [] # each element is a single inner edge with several points
    
    # Go through all contours and hierarchy
    for i, (cnt, hrc) in enumerate(zip(contours, hierarchy[0])):
        # Convert contour points back to original coordinates
        cnt = cnt.reshape(-1, 2)
        
        # Check if it's an outer or inner edge (hierarchy: [Next, Previous, First Child, Parent])
        if hrc[3] == -1:  # it's an outer edge if it has no parent
            outer_edges.append(cnt)
        else:  # it's an inner edge if it has a parent
            inner_edges.append(cnt)
    
    # add edges
    # connect the last point to the first one
    if len(outer_edges) > 0:
        for tmp_plot in outer_edges:
            tmp_plot = np.append(tmp_plot, [tmp_plot[0]], axis=0)
            plt.plot(tmp_plot[:, 0], tmp_plot[:, 1], 'g--')
    
    if len(inner_edges) > 0:
        for tmp_plot in inner_edges:
            tmp_plot = np.append(tmp_plot, [tmp_plot[0]], axis=0)
            plt.plot(tmp_plot[:, 0], tmp_plot[:, 1], 'r--')
            
    # add generated high resolution grid
    sns.scatterplot(data=grid_df, x='x', y='y', marker='X', color='k')
    
    directory = os.path.join(output_path, 'diagnosis', 'imputation')
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    plt.savefig(os.path.join(directory, figname))
    
    plt.close()
    
    
    
    
    