import numpy as np
import pandas as pd
from datetime import datetime
import json
from simulation_core import SimulationEnvironment
from statistical_analysis import (
    perform_anova_analysis, perform_regression_analysis,
    perform_comprehensive_causal_analysis
)
import plotly.graph_objects as go
from plotly.subplots import make_subplots

class BatchExperimentRunner:
    """Run batch experiments with multiple configurations"""
    
    def __init__(self):
        self.experiments = []
        self.results = []
    
    def add_experiment(self, name, config):
        """Add an experiment configuration to the batch"""
        self.experiments.append({
            'name': name,
            'config': config,
            'timestamp': datetime.now().isoformat()
        })
    
    def run_batch(self, progress_callback=None):
        """Run all experiments in the batch"""
        self.results = []
        total_experiments = len(self.experiments)
        
        for idx, experiment in enumerate(self.experiments):
            if progress_callback:
                progress_callback(idx / total_experiments)
            
            result = self._run_single_experiment(experiment)
            self.results.append(result)
        
        if progress_callback:
            progress_callback(1.0)
        
        return self.results
    
    def _run_single_experiment(self, experiment):
        """Run a single experiment"""
        config = experiment['config']
        
        env = SimulationEnvironment(
            world_size=config.get('world_size', 15),
            num_agents=config.get('num_agents', 8),
            num_food=config.get('num_food', 10),
            num_dangers=config.get('num_dangers', 5),
            bandwidth_bits=config.get('bandwidth_bits', 1000),
            vision_radius=config.get('vision_radius', 3)
        )
        
        runs = []
        for run_idx in range(config.get('num_runs', 5)):
            seed = config.get('seed', 42) + run_idx if config.get('seed') is not None else None
            env.initialize(seed=seed)
            
            stats = env.run_episode(num_steps=config.get('num_steps', 30))
            runs.append(stats)
        
        aggregated_stats = self._aggregate_runs(runs)
        
        return {
            'name': experiment['name'],
            'config': config,
            'runs': runs,
            'aggregated': aggregated_stats,
            'timestamp': experiment['timestamp']
        }
    
    def _aggregate_runs(self, runs):
        """Aggregate statistics across multiple runs"""
        efficiencies = [r.get('net_efficiency', 0) for r in runs]
        coord_rates = [r.get('coordination_rate', 0) for r in runs]
        food_collected = [r.get('food_collected', 0) for r in runs]
        dangers_hit = [r.get('dangers_hit', 0) for r in runs]
        msg_delivery_rates = [r.get('message_delivery_rate', 0) for r in runs]
        
        return {
            'efficiency': {
                'mean': np.mean(efficiencies),
                'std': np.std(efficiencies),
                'min': np.min(efficiencies),
                'max': np.max(efficiencies)
            },
            'coordination': {
                'mean': np.mean(coord_rates),
                'std': np.std(coord_rates)
            },
            'food': {
                'mean': np.mean(food_collected),
                'total': sum(food_collected)
            },
            'dangers': {
                'mean': np.mean(dangers_hit),
                'total': sum(dangers_hit)
            },
            'msg_delivery': {
                'mean': np.mean(msg_delivery_rates),
                'std': np.std(msg_delivery_rates)
            }
        }
    
    def generate_comparison_report(self):
        """Generate a comparison report across all experiments"""
        if not self.results:
            return None
        
        report = {
            'summary': self._create_summary_table(),
            'best_performer': self._find_best_performer(),
            'statistical_analysis': self._perform_statistical_comparison()
        }
        
        return report
    
    def _create_summary_table(self):
        """Create summary table of all experiments"""
        rows = []
        for result in self.results:
            agg = result['aggregated']
            rows.append({
                'Experiment': result['name'],
                'Agents': result['config']['num_agents'],
                'Bandwidth': result['config']['bandwidth_bits'],
                'Mean Efficiency': agg['efficiency']['mean'],
                'Std Efficiency': agg['efficiency']['std'],
                'Mean Coordination': agg['coordination']['mean'],
                'Runs': result['config'].get('num_runs', 5)
            })
        
        return pd.DataFrame(rows)
    
    def _find_best_performer(self):
        """Find the best performing experiment"""
        best_idx = max(range(len(self.results)), 
                       key=lambda i: self.results[i]['aggregated']['efficiency']['mean'])
        
        return {
            'name': self.results[best_idx]['name'],
            'efficiency': self.results[best_idx]['aggregated']['efficiency']['mean'],
            'config': self.results[best_idx]['config']
        }
    
    def _perform_statistical_comparison(self):
        """Perform statistical comparison across experiments"""
        if len(self.results) < 2:
            return None
        
        data_records = []
        for result in self.results:
            for run in result['runs']:
                data_records.append({
                    'experiment': result['name'],
                    'efficiency': run.get('net_efficiency', 0),
                    'coordination': run.get('coordination_rate', 0)
                })
        
        df = pd.DataFrame(data_records)
        
        try:
            from statsmodels.formula.api import ols
            from statsmodels.stats.anova import anova_lm
            
            model = ols('efficiency ~ C(experiment)', data=df).fit()
            anova_table = anova_lm(model, typ=2)
            
            return {
                'anova': anova_table,
                'f_statistic': anova_table['F'].iloc[0],
                'p_value': anova_table['PR(>F)'].iloc[0],
                'significant': anova_table['PR(>F)'].iloc[0] < 0.05
            }
        except:
            return None


class AutomatedReportGenerator:
    """Generate automated reports from experiment results"""
    
    def __init__(self, batch_results):
        self.batch_results = batch_results
    
    def generate_full_report(self):
        """Generate a comprehensive report"""
        report = {
            'metadata': self._create_metadata(),
            'executive_summary': self._create_executive_summary(),
            'detailed_results': self._create_detailed_results(),
            'visualizations': self._create_visualizations()
        }
        
        return report
    
    def _create_metadata(self):
        """Create report metadata"""
        return {
            'generated_at': datetime.now().isoformat(),
            'num_experiments': len(self.batch_results),
            'total_runs': sum(r['config'].get('num_runs', 5) for r in self.batch_results)
        }
    
    def _create_executive_summary(self):
        """Create executive summary"""
        efficiencies = [r['aggregated']['efficiency']['mean'] for r in self.batch_results]
        
        best_idx = np.argmax(efficiencies)
        worst_idx = np.argmin(efficiencies)
        
        return {
            'best_experiment': self.batch_results[best_idx]['name'],
            'best_efficiency': efficiencies[best_idx],
            'worst_experiment': self.batch_results[worst_idx]['name'],
            'worst_efficiency': efficiencies[worst_idx],
            'mean_across_all': np.mean(efficiencies),
            'std_across_all': np.std(efficiencies)
        }
    
    def _create_detailed_results(self):
        """Create detailed results table"""
        rows = []
        for result in self.batch_results:
            agg = result['aggregated']
            rows.append({
                'name': result['name'],
                'efficiency_mean': agg['efficiency']['mean'],
                'efficiency_std': agg['efficiency']['std'],
                'coordination_mean': agg['coordination']['mean'],
                'food_mean': agg['food']['mean'],
                'dangers_mean': agg['dangers']['mean'],
                'config': result['config']
            })
        
        return rows
    
    def _create_visualizations(self):
        """Create visualization data"""
        return {
            'efficiency_comparison': self._create_efficiency_plot(),
            'coordination_comparison': self._create_coordination_plot(),
            'radar_chart': self._create_radar_chart()
        }
    
    def _create_efficiency_plot(self):
        """Create efficiency comparison plot"""
        names = [r['name'] for r in self.batch_results]
        means = [r['aggregated']['efficiency']['mean'] for r in self.batch_results]
        stds = [r['aggregated']['efficiency']['std'] for r in self.batch_results]
        
        fig = go.Figure(data=[
            go.Bar(
                x=names,
                y=means,
                error_y=dict(type='data', array=stds),
                marker_color='#3498db'
            )
        ])
        
        fig.update_layout(
            title='Efficiency Comparison Across Experiments',
            xaxis_title='Experiment',
            yaxis_title='Mean Efficiency',
            template='plotly_white'
        )
        
        return fig
    
    def _create_coordination_plot(self):
        """Create coordination comparison plot"""
        names = [r['name'] for r in self.batch_results]
        means = [r['aggregated']['coordination']['mean'] for r in self.batch_results]
        
        fig = go.Figure(data=[
            go.Bar(
                x=names,
                y=means,
                marker_color='#2ecc71'
            )
        ])
        
        fig.update_layout(
            title='Coordination Rate Comparison',
            xaxis_title='Experiment',
            yaxis_title='Mean Coordination Rate',
            yaxis_tickformat='.0%',
            template='plotly_white'
        )
        
        return fig
    
    def _create_radar_chart(self):
        """Create radar chart comparing all metrics"""
        if len(self.batch_results) > 5:
            return None
        
        fig = go.Figure()
        
        categories = ['Efficiency', 'Coordination', 'Food', 'Msg Delivery']
        
        for result in self.batch_results:
            agg = result['aggregated']
            
            values = [
                agg['efficiency']['mean'],
                agg['coordination']['mean'] * 10,
                agg['food']['mean'],
                agg['msg_delivery']['mean'] * 10
            ]
            
            fig.add_trace(go.Scatterpolar(
                r=values,
                theta=categories,
                fill='toself',
                name=result['name']
            ))
        
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True)),
            showlegend=True,
            title='Multi-Metric Comparison',
            template='plotly_white'
        )
        
        return fig


def create_batch_template(template_type='bandwidth_sweep'):
    """Create pre-configured batch experiment templates"""
    templates = {
        'bandwidth_sweep': [
            {'name': 'Low BW', 'config': {'bandwidth_bits': 100, 'num_runs': 5}},
            {'name': 'Medium BW', 'config': {'bandwidth_bits': 1000, 'num_runs': 5}},
            {'name': 'High BW', 'config': {'bandwidth_bits': 10000, 'num_runs': 5}}
        ],
        'agent_scaling': [
            {'name': '4 Agents', 'config': {'num_agents': 4, 'num_runs': 5}},
            {'name': '8 Agents', 'config': {'num_agents': 8, 'num_runs': 5}},
            {'name': '12 Agents', 'config': {'num_agents': 12, 'num_runs': 5}},
            {'name': '16 Agents', 'config': {'num_agents': 16, 'num_runs': 5}}
        ],
        'vision_range': [
            {'name': 'Vision 1', 'config': {'vision_radius': 1, 'num_runs': 5}},
            {'name': 'Vision 3', 'config': {'vision_radius': 3, 'num_runs': 5}},
            {'name': 'Vision 5', 'config': {'vision_radius': 5, 'num_runs': 5}},
            {'name': 'Vision 10', 'config': {'vision_radius': 10, 'num_runs': 5}}
        ]
    }
    
    return templates.get(template_type, [])
