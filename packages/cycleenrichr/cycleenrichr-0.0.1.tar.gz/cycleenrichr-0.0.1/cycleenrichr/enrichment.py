import h5py as h5
import numpy as np
import pandas as pd
import random
import scipy.stats as stats
import tqdm
from statsmodels.stats.multitest import multipletests
from multiprocessing import Pool, cpu_count
import concurrent.futures

def get_network(file_path):
    tissue_network = {}
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line:
                parts = line.split('\t')
                key = parts[0]
                values = parts[1:]
                tissue_network[key] = values
    return tissue_network

def list(px_prediction_file):
    with h5.File(px_prediction_file, 'r') as h5_file:
        predicted_libraries = [key for key in h5_file.keys()]
    print(predicted_libraries)

def enrich(library, px_prediction_file, prediction_libraries=[], verbose=True):
    all_results = {}
    with h5.File(px_prediction_file, 'r') as h5_file:
        predicted_libraries = [key for key in h5_file.keys()]
    if len(prediction_libraries) > 0:
        predicted_libraries = list(set(predicted_libraries) & set(prediction_libraries))
    if len(predicted_libraries) == 0:
        print("no libraries selected. Use cycleenrichr.enrichment.list() to show valid libraries.")
        return 0

    for lib in predicted_libraries:
        with h5.File(px_prediction_file, 'r') as h5_file:
            genes = [x.decode() for x in np.array(h5_file[lib]["gene"])]
            sets = [x.decode() for x in np.array(h5_file[lib]["set"])]
            predictions = pd.DataFrame(h5_file[lib]["prediction"], columns=sets, index=genes)

        all_results[lib] = {}
        
        pbar = tqdm.tqdm(total=len(library.keys()), desc=f"{lib}", disable = not verbose)
        
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_results = {executor.submit(process_library, library, k, genes, predictions, sets): k for k in library.keys()}
            for future in concurrent.futures.as_completed(future_results):
                k = future_results[future]
                try:
                    result = future.result()
                except Exception as e:
                    print(f"Error processing library {k}: {e}")
                else:
                    all_results[lib][k] = result
                finally:
                    # Update the progress bar for each task completed
                    pbar.update(1)
        pbar.close()  # Ensure to close the progress bar after completion

    return all_results

def process_library(library, k, genes, predictions, sets):
    tset = set(library[k])
    z_scores, p_values = get_pvalues(tset, genes, predictions, k=500)
    p_adjusted_bonferroni = multipletests(p_values, method='bonferroni')
    p_adjusted_fdr = multipletests(p_values, method='fdr_bh')
    results = pd.DataFrame([z_scores, p_values, p_adjusted_bonferroni, p_adjusted_fdr], columns=sets, index=["z_score", "p_value", "bonferroni", "fdr"]).T.sort_values(by="p_value", ascending=True)
    return results

def enrich2(library, px_prediction_file, prediction_libraries=[]):
    all_results = {}
    with h5.File(px_prediction_file, 'r') as h5_file:
        predicted_libraries = [key for key in h5_file.keys()]

    if len(prediction_libraries) > 0:
        predicted_libraries = list(set(predicted_libraries) & set(prediction_libraries))
    if len(predicted_libraries) == 0:
        print("no libraries selected. Use cycleenrichr.enrichment.list() to show valid libraries.")
        return 0
    
    for lib in range(len(predicted_libraries)):
        with h5.File(px_prediction_file, 'r') as h5_file:
            genes = [x.decode() for x in np.array(h5_file[predicted_libraries[lib]]["gene"])]
            sets = [x.decode() for x in np.array(h5_file[predicted_libraries[lib]]["set"])]
            predictions = pd.DataFrame(h5_file[predicted_libraries[lib]]["prediction"], columns=sets, index=genes)

        all_results[lib] = {}

        for k in tqdm.tqdm(list(library.keys())):
            tset = set(library[k])
            z_scores, p_values = get_pvalues(tset, genes, predictions, k=500)
            p_adjusted_bonferroni = multipletests(p_values, method='bonferroni')
            p_adjusted_fdr = multipletests(p_values, method='fdr_bh')
            results = pd.DataFrame([z_scores, p_values, p_adjusted_bonferroni, p_adjusted_fdr], 
                       columns = sets, 
                       index=["z_score", "p_value", "bonferroni", "fdr"]
                       ).T.sort_values(by="p_value", ascending=True)
            all_results[lib][k] = results
    
    return all_results

global_lookup = {}

def get_pvalues(gene_set, genes, predictions, k=500):
    idx = [i for i, x in enumerate(genes) if x in gene_set]
    scores = np.mean(predictions.values[idx,:], axis=0)
    means, stds = get_random_scores(idx, predictions, k=k)
    zscores = (scores-means)/stds
    p_values = stats.norm.sf(zscores)
    return zscores, p_values

def get_random_scores(idx, predictions, k=500):
    l = len(idx)
    m = range(predictions.shape[0])
    res = []
    for i in range(k):
        res.append(predictions.values[random.sample(m, l)].mean(axis=0))
    zm = np.mean(np.array(res), axis=0)
    zstd = np.std(np.array(res), axis=0)
    return zm, zstd