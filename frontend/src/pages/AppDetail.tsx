import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import {
  Card,
  Button,
  Typography,
  Row,
  Col,
  Tag,
  Divider,
  Tabs,
  Rate,
  message,
  Spin,
} from 'antd';
import {
  DownloadOutlined,
  RocketOutlined,
  StarOutlined,
  UserOutlined,
} from '@ant-design/icons';
import { applicationsAPI, installationsAPI } from '../api/client';
import ReactECharts from 'echarts-for-react';

const { Title, Paragraph, Text } = Typography;
const { TabPane } = Tabs;

const AppDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [app, setApp] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [installing, setInstalling] = useState(false);

  useEffect(() => {
    if (id) {
      loadApplication(id);
    }
  }, [id]);

  const loadApplication = async (appId: string) => {
    setLoading(true);
    try {
      const response = await applicationsAPI.get(appId);
      setApp(response.data);
    } catch (error) {
      message.error('加载应用详情失败');
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const handleInstall = async () => {
    if (!id) return;

    setInstalling(true);
    try {
      await installationsAPI.install(id);
      message.success('安装成功！');
      // Reload app to update install count
      loadApplication(id);
    } catch (error) {
      message.error('安装失败');
      console.error(error);
    } finally {
      setInstalling(false);
    }
  };

  if (loading) {
    return (
      <div style={{ textAlign: 'center', padding: '100px 0' }}>
        <Spin size="large" />
      </div>
    );
  }

  if (!app) {
    return <div>应用不存在</div>;
  }

  const usageChartOption = {
    title: {
      text: '使用统计（最近 30 天）',
    },
    tooltip: {
      trigger: 'axis',
    },
    xAxis: {
      type: 'category',
      data: ['Day1', 'Day2', 'Day3', 'Day4', 'Day5', 'Day6', 'Day7'],
    },
    yAxis: {
      type: 'value',
    },
    series: [
      {
        name: '调用次数',
        type: 'line',
        data: [120, 200, 150, 80, 70, 110, 130],
      },
    ],
  };

  return (
    <div style={{ padding: '24px' }}>
      <Row gutter={24}>
        <Col span={18}>
          <Card>
            <div style={{ display: 'flex', alignItems: 'flex-start' }}>
              <div
                style={{
                  width: 80,
                  height: 80,
                  background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                  borderRadius: 8,
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  fontSize: 40,
                  marginRight: 16,
                }}
              >
                {app.type === 'agent' ? '🤖' : '⚡'}
              </div>
              <div style={{ flex: 1 }}>
                <Title level={2}>{app.display_name}</Title>
                <div>
                  <Rate disabled defaultValue={app.rating_avg} />
                  <Text type="secondary" style={{ marginLeft: 8 }}>
                    {app.rating_avg.toFixed(1)} ({app.rating_count} 评价)
                  </Text>
                </div>
                <div style={{ marginTop: 8 }}>
                  <Text type="secondary">
                    <UserOutlined /> {app.publisher_name}
                  </Text>
                  {app.publisher_dept && (
                    <Text type="secondary" style={{ marginLeft: 16 }}>
                      | {app.publisher_dept}
                    </Text>
                  )}
                </div>
              </div>
            </div>

            <Divider />

            <Tabs defaultActiveKey="overview">
              <TabPane tab="概览" key="overview">
                <Title level={4}>功能描述</Title>
                <Paragraph>{app.description}</Paragraph>

                <Title level={4}>分类</Title>
                <Tag color="blue">{app.category}</Tag>
                {app.tags && app.tags.map((tag: string) => <Tag key={tag}>{tag}</Tag>)}

                <Divider />

                <Title level={4}>使用统计</Title>
                <ReactECharts option={usageChartOption} style={{ height: 400 }} />
              </TabPane>

              <TabPane tab="版本历史" key="versions">
                <Paragraph>版本信息正在开发中...</Paragraph>
              </TabPane>

              <TabPane tab="用户评价" key="reviews">
                <Paragraph>评价功能正在开发中...</Paragraph>
              </TabPane>
            </Tabs>
          </Card>
        </Col>

        <Col span={6}>
          <Card>
            <Button
              type="primary"
              size="large"
              icon={<RocketOutlined />}
              block
              onClick={handleInstall}
              loading={installing}
            >
              一键安装
            </Button>
            <Button
              size="large"
              icon={<DownloadOutlined />}
              block
              style={{ marginTop: 8 }}
            >
              下载压缩包
            </Button>
            <Button size="large" icon={<StarOutlined />} block style={{ marginTop: 8 }}>
              收藏
            </Button>

            <Divider />

            <div>
              <Text type="secondary">安装次数</Text>
              <div>
                <Text strong style={{ fontSize: 24 }}>
                  {app.install_count}
                </Text>
              </div>
            </div>

            <Divider />

            <div>
              <Text type="secondary">下载次数</Text>
              <div>
                <Text strong style={{ fontSize: 24 }}>
                  {app.download_count}
                </Text>
              </div>
            </div>
          </Card>
        </Col>
      </Row>
    </div>
  );
};

export default AppDetailPage;
