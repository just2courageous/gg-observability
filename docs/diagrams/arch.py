import os
from graphviz import Digraph

# Requirements:
# 1. pip install graphviz
# 2. Graphviz must be installed on your system (dot command on PATH)

def generate_perfect_diagram():
    # 1. Ensure output directory exists
    output_dir = "docs/diagrams"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 2. Initialize Digraph with Dark Theme global attributes
    dot = Digraph('gg-observability', comment='Observability Stack')
    dot.attr(
        rankdir='LR',
        bgcolor='#121212',  # Deep dark background
        fontcolor='#E0E0E0',
        fontname='Verdana',
        fontsize='20',
        pad='0.5',
        nodesep='0.6',
        ranksep='1.0',
        splines='ortho'
    )

    # Global Node Styles
    dot.attr('node',
             shape='rect',
             style='filled,rounded',
             fillcolor='#1E1E1E',
             color='#333333',
             fontcolor='#FFFFFF',
             fontname='Verdana',
             fontsize='12')

    # Global Edge Styles
    dot.attr('edge', color='#666666', fontcolor='#AAAAAA', fontname='Verdana', fontsize='10')

    # --- LEFT SIDE: ACCESS LAYER ---
    with dot.subgraph(name='cluster_access') as c:
        c.attr(label='Local Access (No Ingress)', color='#444444', fontcolor='#888888', style='dotted')
        c.node('browser', 'User Browser\n(localhost)', shape='circle', fillcolor='#0D47A1')
        c.node('port_forward', 'kubectl port-forward', shape='parallelogram', fillcolor='#1B5E20')

    # --- RIGHT SIDE: CLOUD STACK ---
    with dot.subgraph(name='cluster_aws') as aws:
        aws.attr(label='AWS', color='#FF9900', fontcolor='#FF9900', style='dashed')
        
        with aws.subgraph(name='cluster_eks') as eks:
            eks.attr(label='EKS Cluster', color='#2E7D32', fontcolor='#81C784', style='rounded')
            
            with eks.subgraph(name='cluster_monitoring') as mon:
                mon.attr(label='Namespace: monitoring', color='#0277BD', fontcolor='#4FC3F7', style='filled', fillcolor='#181818')
                
                # Release kps components
                mon.node('operator', 'Prometheus Operator', fillcolor='#D84315')
                mon.node('prom', 'Prometheus\n(release: kps)', fillcolor='#E65100', penwidth='2')
                mon.node('alertmanager', 'Alertmanager', fillcolor='#BF360C')
                mon.node('grafana', 'Grafana\n(Admin Secret: kps-grafana-admin)', fillcolor='#F4511E')
                mon.node('ksm', 'kube-state-metrics', fillcolor='#1565C0')
                mon.node('node_exporter', 'node-exporter', fillcolor='#1565C0')
                
                # Alert Rule
                mon.node('demo_alerts', 'PrometheusRule\n"demo-alerts"', shape='note', fillcolor='#4A148C')

    # --- FLOWS ---
    # Access paths
    dot.edge('browser', 'port_forward')
    dot.edge('port_forward', 'grafana', label='tunnel :3000', color='#F4511E')
    dot.edge('port_forward', 'prom', label='tunnel :9090', color='#E65100')

    # Internal Monitoring logic
    dot.edge('node_exporter', 'prom', label='scrape metrics')
    dot.edge('ksm', 'prom', label='scrape k8s stats')
    dot.edge('demo_alerts', 'prom', label='rule evaluation', style='dashed')
    dot.edge('prom', 'alertmanager', label='firing alerts')
    dot.edge('grafana', 'prom', label='query (PromQL)')

    # 3. Render
    output_path = f"{output_dir}/gg-observability-arch"
    dot.render(output_path, format='png', cleanup=True)
    
    # Render DOT separately if needed
    dot.save(f"{output_path}.dot")
    
    print(f"Wrote: {output_path}.png")

if __name__ == "__main__":
    generate_perfect_diagram()