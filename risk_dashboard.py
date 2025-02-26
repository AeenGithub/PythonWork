import dash
from dash import html, dcc
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import pandas as pd

# 初始化Dash应用
app = dash.Dash(__name__)

# 模拟数据
def generate_sample_data():
    # 问题数量统计数据
    problem_stats = {
        '类别': ['质量', '生产制造', '能源与环保', '安全', '人力资源'],
        '数量': [123, 115, 90, 59, 33]
    }
    
    # 风险事件数据
    risk_events = {
        '每百万销值事故率': 2.5,
        '事件统计': [
            {'事件类型': '特大事件', '数量': 0},
            {'事件类型': '重大事件', '数量': 2},
            {'事件类型': '较大事件', '数量': 48}
        ],
        '问题清单': [
            {
                '标题': '某工厂发生安全生产事故',
                '处理部门': '安全生产部',
                '状态': '处理中',
                '链接': 'http://example.com/detail/1'
            },
            {
                '标题': '产品质量异常事件',
                '处理部门': '质量管理部',
                '状态': '已完成',
                '链接': 'http://example.com/detail/2'
            },
            {
                '标题': '环保设备故障事件',
                '处理部门': '设备管理部',
                '状态': '处理中',
                '链接': 'http://example.com/detail/3'
            }
        ]
    }
    
    # 风险成熟度排行数据
    risk_maturity = [
        {'公司': '高明产业园公司', '2024': 1, '2025': 3},
        {'公司': '南宁产业园公司', '2024': 2, '2025': 1},
        {'公司': '清江产业园公司', '2024': 3, '2025': 4},
        {'公司': '武汉产业园公司', '2024': 4, '2025': 2},
        {'公司': '红河公众食品有限公司', '2024': 5, '2025': 6}
    ]
    
    return pd.DataFrame(problem_stats), risk_events, pd.DataFrame(risk_maturity)

# 创建图表
def create_problem_stats_chart(df):
    fig = go.Figure(data=[go.Bar(
        x=df['类别'],
        y=df['数量'],
        marker_color='#00ffff'
    )])
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#ffffff',
        margin=dict(l=20, r=20, t=30, b=20),
        height=300
    )
    
    return fig

# 应用布局
app.layout = html.Div([
    # 标题
    html.H1('风控驾驶舱', style={
        'textAlign': 'center',
        'color': '#00ffff',
        'marginBottom': '20px'
    }),
    
    # 顶部筛选器
    html.Div([
        html.Div([
            dcc.Dropdown(
                id='filter-1',
                options=[{'label': '选项1', 'value': '1'}],
                placeholder='筛选项1'
            )
        ], style={'width': '19%', 'display': 'inline-block', 'marginRight': '1%'}),
        html.Div([
            dcc.Dropdown(
                id='filter-2',
                options=[{'label': '选项2', 'value': '2'}],
                placeholder='筛选项2'
            )
        ], style={'width': '19%', 'display': 'inline-block', 'marginRight': '1%'}),
        html.Div([
            dcc.Dropdown(
                id='filter-3',
                options=[{'label': '选项3', 'value': '3'}],
                placeholder='筛选项3'
            )
        ], style={'width': '19%', 'display': 'inline-block', 'marginRight': '1%'}),
        html.Div([
            dcc.Dropdown(
                id='filter-4',
                options=[{'label': '选项4', 'value': '4'}],
                placeholder='筛选项4'
            )
        ], style={'width': '19%', 'display': 'inline-block', 'marginRight': '1%'}),
        html.Div([
            dcc.Dropdown(
                id='filter-5',
                options=[{'label': '选项5', 'value': '5'}],
                placeholder='筛选项5'
            )
        ], style={'width': '19%', 'display': 'inline-block'})
    ], style={'marginBottom': '20px'}),
    
    # 内容模块网格布局
    html.Div([
        # 第一行
        html.Div([
            # 问题数量统计
            html.Div([
                html.H3('问题数量统计(Top5模块)', style={'color': '#ffffff'}),
                dcc.Graph(id='problem-stats')
            ], style={'width': 'calc(33.33% - 20px)', 'height': '400px', 'display': 'inline-block', 'marginRight': '30px', 'backgroundColor': '#002b56', 'padding': '20px', 'borderRadius': '5px', 'verticalAlign': 'top'}),
            
            # 风险大事记
            html.Div([
                html.H3('风险大事记', style={'color': '#ffffff'}),
                html.Div([
                    html.H4('每百万销值事故率', style={'color': '#00ffff', 'marginBottom': '10px'}),
                    html.Div(id='accident-rate', style={'fontSize': '24px', 'color': '#ffffff'})
                ], style={'marginBottom': '20px', 'textAlign': 'center'}),
                html.Div([
                    html.H4('事件统计', style={'color': '#00ffff', 'marginBottom': '10px'}),
                    html.Div(id='event-stats', style={'color': '#ffffff'})
                ], style={'marginBottom': '20px'}),
                html.Div([
                    html.H4('问题清单', style={'color': '#00ffff', 'marginBottom': '10px'}),
                    html.Div(id='issue-list', style={'color': '#ffffff', 'overflowY': 'auto', 'maxHeight': '150px'})
                ])
            ], style={'width': 'calc(33.33% - 20px)', 'height': '400px', 'display': 'inline-block', 'marginRight': '30px', 'backgroundColor': '#002b56', 'padding': '20px', 'borderRadius': '5px', 'verticalAlign': 'top'}),
            
            # 订阅服务
            html.Div([
                html.H3('订阅服务', style={'color': '#ffffff'}),
                html.Div(id='order-service', style={'color': '#ffffff'})
            ], style={'width': 'calc(33.33% - 20px)', 'height': '400px', 'display': 'inline-block', 'backgroundColor': '#002b56', 'padding': '20px', 'borderRadius': '5px', 'verticalAlign': 'top'})
        ], style={'marginBottom': '30px'}),
        
        # 第二行
        html.Div([
            # 问题整改情况
            html.Div([
                html.H3('问题整改情况', style={'color': '#ffffff'}),
                html.Div(id='issue-improvement', style={'color': '#ffffff'})
            ], style={'width': 'calc(33.33% - 20px)', 'height': '400px', 'display': 'inline-block', 'marginRight': '30px', 'backgroundColor': '#002b56', 'padding': '20px', 'borderRadius': '5px', 'verticalAlign': 'top'}),
            
            # 高频问题
            html.Div([
                html.H3('高频问题', style={'color': '#ffffff'}),
                html.Div(id='frequent-issues', style={'color': '#ffffff'})
            ], style={'width': 'calc(33.33% - 20px)', 'height': '400px', 'display': 'inline-block', 'marginRight': '30px', 'backgroundColor': '#002b56', 'padding': '20px', 'borderRadius': '5px', 'verticalAlign': 'top'}),
            
            # 风控成熟度排行榜
            html.Div([
                html.H3('风控成熟度排行榜', style={'color': '#ffffff'}),
                html.Div(id='risk-maturity', style={'color': '#ffffff'})
            ], style={'width': 'calc(33.33% - 20px)', 'height': '400px', 'display': 'inline-block', 'backgroundColor': '#002b56', 'padding': '20px', 'borderRadius': '5px', 'verticalAlign': 'top'})
        ])
    ])
], style={
    'backgroundColor': '#001f3f',
    'padding': '20px'
})

# 回调函数更新图表和数据
@app.callback(
    [
        Output('problem-stats', 'figure'),
        Output('accident-rate', 'children'),
        Output('event-stats', 'children'),
        Output('issue-list', 'children')
    ],
    Input('problem-stats', 'id')
)
def update_dashboard(id):
    df_stats, risk_events, _ = generate_sample_data()
    
    # 更新问题统计图表
    fig = create_problem_stats_chart(df_stats)
    
    # 更新事故率
    accident_rate = f"{risk_events['每百万销值事故率']}%"
    
    # 更新事件统计
    event_stats = html.Div([
        html.Div([
            html.Span(event['事件类型'] + ': ', style={'marginRight': '5px'}),
            html.Span(str(event['数量']))
        ], style={'marginBottom': '5px'}) 
        for event in risk_events['事件统计']
    ])
    
    # 更新问题清单
    issue_list = html.Div([
        html.Div([
            html.Div(issue['标题'], style={'fontWeight': 'bold', 'marginBottom': '5px'}),
            html.Div([
                html.Span('处理部门: ' + issue['处理部门'], style={'marginRight': '10px'}),
                html.Span('状态: ' + issue['状态'], style={'marginRight': '10px'}),
                html.A('查看详情', href=issue['链接'], target='_blank',
                       style={'color': '#00ffff', 'textDecoration': 'none'})
            ], style={'fontSize': '0.9em'})
        ], style={'marginBottom': '15px', 'padding': '10px', 'border': '1px solid #00ffff'})
        for issue in risk_events['问题清单']
    ])
    
    return fig, accident_rate, event_stats, issue_list

# 启动服务器
if __name__ == '__main__':
    app.run_server(debug=True)