import React, { useEffect, useState } from 'react';
import { Card, Row, Col, Typography, Tabs, Input, Select, Spin, message } from 'antd';
import { StarFilled, DownloadOutlined, FireOutlined, ClockCircleOutlined } from '@ant-design/icons';
import { applicationsAPI } from '../api/client';
import { useNavigate } from 'react-router-dom';

const { Title, Paragraph, Text } = Typography;
const { Search } = Input;
const { TabPane } = Tabs;

const HomePage: React.FC = () => {
  const [applications, setApplications] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState('all');
  const [searchText, setSearchText] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    loadApplications();
  }, [activeTab, searchText]);

  const loadApplications = async () => {
    setLoading(true);
    try {
      const params: any = {
        page: 1,
        page_size: 20,
      };

      if (activeTab !== 'all') {
        params.type = activeTab;
      }

      if (searchText) {
        params.search = searchText;
      }

      const response = await applicationsAPI.list(params);
      setApplications(response.data.data);
    } catch (error) {
      message.error('加载应用失败');
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const handleCardClick = (appId: string) => {
    navigate(`/app/${appId}`);
  };

  return (
    <div style={{ padding: '24px' }}>
      <div style={{ marginBottom: '32px' }}>
        <Title level={2}>SA Market</Title>
        <Paragraph>探索智能化的 Agents 和 Skills</Paragraph>
      </div>

      <div style={{ marginBottom: '24px' }}>
        <Row gutter={16}>
          <Col span={18}>
            <Search
              placeholder="搜索应用名称、描述..."
              allowClear
              size="large"
              onSearch={setSearchText}
              style={{ width: '100%' }}
            />
          </Col>
          <Col span={6}>
            <Select
              defaultValue="latest"
              size="large"
              style={{ width: '100%' }}
              options={[
                { value: 'latest', label: '最新发布' },
                { value: 'popular', label: '热门应用' },
                { value: 'rating', label: '评分最高' },
              ]}
            />
          </Col>
        </Row>
      </div>

      <Tabs activeKey={activeTab} onChange={setActiveTab}>
        <TabPane tab="全部" key="all" />
        <TabPane tab="🤖 Agents" key="agent" />
        <TabPane tab="⚡ Skills" key="skill" />
      </Tabs>

      <Spin spinning={loading}>
        <Row gutter={[16, 16]}>
          {applications.map((app) => (
            <Col key={app.id} xs={24} sm={12} md={8} lg={6}>
              <Card
                hoverable
                onClick={() => handleCardClick(app.id)}
                cover={
                  <div
                    style={{
                      height: 160,
                      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      fontSize: 48,
                    }}
                  >
                    {app.type === 'agent' ? '🤖' : '⚡'}
                  </div>
                }
              >
                <Card.Meta
                  title={app.display_name}
                  description={
                    <div>
                      <Paragraph ellipsis={{ rows: 2 }} style={{ marginBottom: 8 }}>
                        {app.description}
                      </Paragraph>
                      <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                        <Text type="secondary">
                          <StarFilled style={{ color: '#faad14' }} /> {app.rating_avg.toFixed(1)}
                        </Text>
                        <Text type="secondary">
                          <DownloadOutlined /> {app.install_count}
                        </Text>
                      </div>
                    </div>
                  }
                />
              </Card>
            </Col>
          ))}
        </Row>
      </Spin>

      {!loading && applications.length === 0 && (
        <div style={{ textAlign: 'center', padding: '60px 0' }}>
          <Text type="secondary">暂无应用</Text>
        </div>
      )}
    </div>
  );
};

export default HomePage;
