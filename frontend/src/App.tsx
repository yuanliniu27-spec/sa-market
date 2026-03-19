import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { Layout, Menu } from 'antd';
import {
  HomeOutlined,
  AppstoreOutlined,
  UploadOutlined,
  UserOutlined,
} from '@ant-design/icons';
import HomePage from './pages/Home';
import AppDetailPage from './pages/AppDetail';
import PublishPage from './pages/Publish';
import './App.css';

const { Header, Content, Footer } = Layout;

const App: React.FC = () => {
  return (
    <Router>
      <Layout style={{ minHeight: '100vh' }}>
        <Header style={{ position: 'fixed', zIndex: 1, width: '100%' }}>
          <div style={{ float: 'left', color: 'white', fontSize: 20, fontWeight: 'bold' }}>
            SA Market
          </div>
          <Menu
            theme="dark"
            mode="horizontal"
            defaultSelectedKeys={['home']}
            style={{ float: 'right' }}
          >
            <Menu.Item key="home" icon={<HomeOutlined />}>
              <Link to="/">首页</Link>
            </Menu.Item>
            <Menu.Item key="publish" icon={<UploadOutlined />}>
              <Link to="/publish">发布</Link>
            </Menu.Item>
            <Menu.Item key="my" icon={<UserOutlined />}>
              <Link to="/my">我的</Link>
            </Menu.Item>
          </Menu>
        </Header>

        <Content style={{ marginTop: 64 }}>
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/app/:id" element={<AppDetailPage />} />
            <Route path="/publish" element={<PublishPage />} />
          </Routes>
        </Content>

        <Footer style={{ textAlign: 'center' }}>
          SA Market ©2026 Created by Li Xiang Auto
        </Footer>
      </Layout>
    </Router>
  );
};

export default App;
