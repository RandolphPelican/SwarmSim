import numpy as np
import pandas as pd
from scipy import stats
from scipy.optimize import curve_fit
import statsmodels.api as sm
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm
from statsmodels.stats.multicomp import pairwise_tukeyhsd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def quadratic_func(x, a, b, c):
    """Quadratic function for inverted U-curve fitting"""
    return a * x**2 + b * x + c

def log_quadratic_func(x, a, b, c):
    """Quadratic function in log space"""
    log_x = np.log(x)
    return a * log_x**2 + b * log_x + c

def perform_anova_analysis(bandwidth_results):
    """Perform one-way ANOVA across bandwidth groups"""
    if not bandwidth_results or len(bandwidth_results) < 2:
        return None
    
    data_records = []
    for result in bandwidth_results:
        bandwidth = result['bandwidth']
        for efficiency in result['efficiencies']:
            data_records.append({
                'bandwidth': bandwidth,
                'bandwidth_group': f'BW_{bandwidth}',
                'efficiency': efficiency
            })
    
    df = pd.DataFrame(data_records)
    
    model = ols('efficiency ~ C(bandwidth_group)', data=df).fit()
    anova_table = anova_lm(model, typ=2)
    
    f_statistic = anova_table['F'].iloc[0]
    p_value = anova_table['PR(>F)'].iloc[0]
    
    tukey_result = pairwise_tukeyhsd(
        endog=df['efficiency'],
        groups=df['bandwidth_group'],
        alpha=0.05
    )
    
    return {
        'anova_table': anova_table,
        'f_statistic': f_statistic,
        'p_value': p_value,
        'tukey_hsd': tukey_result,
        'significant': p_value < 0.05,
        'dataframe': df
    }

def perform_regression_analysis(bandwidth_results):
    """Perform regression analysis to test for inverted U-curve"""
    if not bandwidth_results or len(bandwidth_results) < 3:
        return None
    
    bandwidths = np.array([r['bandwidth'] for r in bandwidth_results])
    efficiencies = np.array([r['mean_efficiency'] for r in bandwidth_results])
    
    linear_model = np.polyfit(np.log(bandwidths), efficiencies, 1)
    linear_pred = np.poly1d(linear_model)(np.log(bandwidths))
    linear_r2 = 1 - (np.sum((efficiencies - linear_pred)**2) / 
                     np.sum((efficiencies - np.mean(efficiencies))**2))
    
    try:
        quad_params, _ = curve_fit(log_quadratic_func, bandwidths, efficiencies)
        quad_pred = log_quadratic_func(bandwidths, *quad_params)
        quad_r2 = 1 - (np.sum((efficiencies - quad_pred)**2) / 
                       np.sum((efficiencies - np.mean(efficiencies))**2))
        
        has_inverted_u = quad_params[0] < 0
        
        optimal_bw = None
        if has_inverted_u:
            optimal_log_bw = -quad_params[1] / (2 * quad_params[0])
            optimal_bw = np.exp(optimal_log_bw)
    except:
        quad_params = None
        quad_r2 = None
        has_inverted_u = False
        optimal_bw = None
    
    X = sm.add_constant(np.column_stack([
        np.log(bandwidths),
        np.log(bandwidths)**2
    ]))
    
    ols_model = sm.OLS(efficiencies, X).fit()
    
    return {
        'linear_coef': linear_model,
        'linear_r2': linear_r2,
        'quadratic_params': quad_params,
        'quadratic_r2': quad_r2,
        'has_inverted_u': has_inverted_u,
        'optimal_bandwidth': optimal_bw,
        'ols_model': ols_model,
        'ols_summary': ols_model.summary(),
        'bandwidths': bandwidths,
        'efficiencies': efficiencies
    }

def perform_paired_t_test(phase_a_data, phase_b_data):
    """Perform paired t-test between two phases"""
    if len(phase_a_data) != len(phase_b_data):
        return stats.ttest_ind(phase_a_data, phase_b_data)
    else:
        return stats.ttest_rel(phase_a_data, phase_b_data)

def calculate_effect_size(phase_a_data, phase_b_data):
    """Calculate Cohen's d effect size"""
    mean_diff = np.mean(phase_a_data) - np.mean(phase_b_data)
    pooled_std = np.sqrt((np.var(phase_a_data) + np.var(phase_b_data)) / 2)
    
    if pooled_std == 0:
        return 0
    
    cohens_d = mean_diff / pooled_std
    
    if abs(cohens_d) < 0.2:
        interpretation = "negligible"
    elif abs(cohens_d) < 0.5:
        interpretation = "small"
    elif abs(cohens_d) < 0.8:
        interpretation = "medium"
    else:
        interpretation = "large"
    
    return {
        'cohens_d': cohens_d,
        'interpretation': interpretation,
        'mean_diff': mean_diff
    }

def perform_comprehensive_causal_analysis(causal_results):
    """Perform comprehensive statistical analysis of causal test results"""
    phase_a = causal_results['phase_a']['efficiencies']
    phase_b = causal_results['phase_b']['efficiencies']
    phase_c = causal_results['phase_c']['efficiencies']
    
    t_ab, p_ab = perform_paired_t_test(phase_a, phase_b)
    t_bc, p_bc = perform_paired_t_test(phase_b, phase_c)
    t_ac, p_ac = perform_paired_t_test(phase_a, phase_c)
    
    effect_ab = calculate_effect_size(phase_a, phase_b)
    effect_bc = calculate_effect_size(phase_b, phase_c)
    effect_ac = calculate_effect_size(phase_a, phase_c)
    
    data_records = []
    for eff in phase_a:
        data_records.append({'phase': 'A', 'efficiency': eff})
    for eff in phase_b:
        data_records.append({'phase': 'B', 'efficiency': eff})
    for eff in phase_c:
        data_records.append({'phase': 'C', 'efficiency': eff})
    
    df = pd.DataFrame(data_records)
    model = ols('efficiency ~ C(phase)', data=df).fit()
    anova_table = anova_lm(model, typ=2)
    
    return {
        't_test_a_vs_b': {'t': t_ab, 'p': p_ab},
        't_test_b_vs_c': {'t': t_bc, 'p': p_bc},
        't_test_a_vs_c': {'t': t_ac, 'p': p_ac},
        'effect_size_a_vs_b': effect_ab,
        'effect_size_b_vs_c': effect_bc,
        'effect_size_a_vs_c': effect_ac,
        'anova': anova_table,
        'overall_f': anova_table['F'].iloc[0],
        'overall_p': anova_table['PR(>F)'].iloc[0]
    }

def create_regression_plot(regression_results):
    """Create visualization of regression analysis"""
    if not regression_results:
        return None
    
    bandwidths = regression_results['bandwidths']
    efficiencies = regression_results['efficiencies']
    
    bw_range = np.logspace(np.log10(bandwidths.min()), 
                           np.log10(bandwidths.max()), 100)
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=bandwidths,
        y=efficiencies,
        mode='markers',
        name='Observed Data',
        marker=dict(size=12, color='#3498db')
    ))
    
    if regression_results['quadratic_params'] is not None:
        quad_pred = log_quadratic_func(bw_range, *regression_results['quadratic_params'])
        
        fig.add_trace(go.Scatter(
            x=bw_range,
            y=quad_pred,
            mode='lines',
            name=f"Quadratic Fit (R² = {regression_results['quadratic_r2']:.3f})",
            line=dict(color='#e74c3c', width=3)
        ))
        
        if regression_results['optimal_bandwidth']:
            opt_bw = regression_results['optimal_bandwidth']
            opt_eff = log_quadratic_func(opt_bw, *regression_results['quadratic_params'])
            
            fig.add_trace(go.Scatter(
                x=[opt_bw],
                y=[opt_eff],
                mode='markers',
                name='Optimal Point',
                marker=dict(size=15, color='#2ecc71', symbol='star')
            ))
    
    fig.update_layout(
        title='Regression Analysis: Bandwidth vs. Efficiency',
        xaxis_title='Bandwidth (bits)',
        yaxis_title='Efficiency',
        xaxis_type='log',
        template='plotly_white',
        height=500,
        hovermode='closest'
    )
    
    return fig

def create_anova_boxplot(anova_results):
    """Create boxplot visualization for ANOVA results"""
    if not anova_results:
        return None
    
    df = anova_results['dataframe']
    
    fig = go.Figure()
    
    for group in df['bandwidth_group'].unique():
        group_data = df[df['bandwidth_group'] == group]['efficiency']
        
        fig.add_trace(go.Box(
            y=group_data,
            name=group.replace('BW_', ''),
            boxmean='sd'
        ))
    
    fig.update_layout(
        title=f'ANOVA Analysis: F = {anova_results["f_statistic"]:.2f}, p = {anova_results["p_value"]:.4f}',
        yaxis_title='Efficiency',
        xaxis_title='Bandwidth (bits)',
        template='plotly_white',
        height=450
    )
    
    return fig

def create_effect_size_plot(causal_analysis):
    """Create visualization of effect sizes"""
    if not causal_analysis:
        return None
    
    comparisons = ['A vs B\n(Remove)', 'B vs C\n(Restore)', 'A vs C\n(Consistency)']
    cohens_d = [
        causal_analysis['effect_size_a_vs_b']['cohens_d'],
        causal_analysis['effect_size_b_vs_c']['cohens_d'],
        causal_analysis['effect_size_a_vs_c']['cohens_d']
    ]
    
    colors = ['#e74c3c', '#2ecc71', '#95a5a6']
    
    fig = go.Figure(data=[
        go.Bar(
            x=comparisons,
            y=cohens_d,
            marker_color=colors,
            text=[f"{d:.2f}" for d in cohens_d],
            textposition='outside'
        )
    ])
    
    fig.add_hline(y=0.2, line_dash="dash", line_color="gray", 
                  annotation_text="Small effect")
    fig.add_hline(y=0.5, line_dash="dash", line_color="gray",
                  annotation_text="Medium effect")
    fig.add_hline(y=0.8, line_dash="dash", line_color="gray",
                  annotation_text="Large effect")
    
    fig.update_layout(
        title="Effect Sizes (Cohen's d)",
        yaxis_title="Cohen's d",
        template='plotly_white',
        height=450
    )
    
    return fig

def generate_statistical_report(bandwidth_results=None, causal_results=None):
    """Generate comprehensive statistical analysis report"""
    report = {
        'sections': []
    }
    
    if bandwidth_results:
        anova = perform_anova_analysis(bandwidth_results)
        regression = perform_regression_analysis(bandwidth_results)
        
        report['sections'].append({
            'title': 'Bandwidth Sweep Analysis',
            'anova': anova,
            'regression': regression
        })
    
    if causal_results:
        causal_stats = perform_comprehensive_causal_analysis(causal_results)
        
        report['sections'].append({
            'title': 'Causal Ablation Analysis',
            'statistics': causal_stats
        })
    
    return report
