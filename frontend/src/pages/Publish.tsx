import React, { useState } from 'react';
import {
  Card,
  Form,
  Input,
  Button,
  Upload,
  Select,
  Typography,
  Steps,
  message,
  Progress,
} from 'antd';
import { UploadOutlined, InboxOutlined } from '@ant-design/icons';
import { applicationsAPI, versionsAPI } from '../api/client';
import { useNavigate } from 'react-router-dom';

const { Title, Paragraph } = Typography;
const { TextArea } = Input;
const { Dragger } = Upload;

const PublishPage: React.FC = () => {
  const [form] = Form.useForm();
  const [currentStep, setCurrentStep] = useState(0);
  const [appId, setAppId] = useState<string>('');
  const [uploading, setUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const navigate = useNavigate();

  const handleBasicInfoSubmit = async (values: any) => {
    try {
      const response = await applicationsAPI.create(values);
      setAppId(response.data.id);
      setCurrentStep(1);
      message.success('基本信息保存成功');
    } catch (error) {
      message.error('保存失败');
      console.error(error);
    }
  };

  const handleFileUpload = async (file: File, values: any) => {
    if (!appId) {
      message.error('请先完成基本信息填写');
      return;
    }

    setUploading(true);
    setUploadProgress(0);

    const formData = new FormData();
    formData.append('app_id', appId);
    formData.append('version', values.version);
    formData.append('changelog', values.changelog || '');
    formData.append('file', file);

    try {
      const response = await versionsAPI.upload(formData);
      setUploadProgress(100);
      message.success('上传成功，正在进行自动审核...');

      // Navigate to audit status page
      setTimeout(() => {
        navigate(`/audit/${response.data.version_id}`);
      }, 2000);
    } catch (error) {
      message.error('上传失败');
      console.error(error);
    } finally {
      setUploading(false);
    }
  };

  const uploadProps = {
    name: 'file',
    multiple: false,
    accept: '.zip',
    beforeUpload: (file: File) => {
      const isZip = file.name.endsWith('.zip');
      if (!isZip) {
        message.error('只能上传 .zip 文件！');
      }
      const isLt50M = file.size / 1024 / 1024 < 50;
      if (!isLt50M) {
        message.error('文件大小不能超过 50MB！');
      }
      return isZip && isLt50M;
    },
  };

  return (
    <div style={{ padding: '24px', maxWidth: 800, margin: '0 auto' }}>
      <Title level={2}>📤 发布新应用</Title>

      <Steps current={currentStep} style={{ marginBottom: 32 }}>
        <Steps.Step title="基本信息" />
        <Steps.Step title="上传代码包" />
        <Steps.Step title="审核中" />
      </Steps>

      {currentStep === 0 && (
        <Card title="第 1 步：基本信息">
          <Form form={form} layout="vertical" onFinish={handleBasicInfoSubmit}>
            <Form.Item
              name="type"
              label="应用类型"
              rules={[{ required: true, message: '请选择应用类型' }]}
            >
              <Select
                options={[
                  { value: 'agent', label: '🤖 Agent' },
                  { value: 'skill', label: '⚡ Skill' },
                ]}
              />
            </Form.Item>

            <Form.Item
              name="name"
              label="应用名称（英文标识）"
              rules={[{ required: true, message: '请输入应用名称' }]}
            >
              <Input placeholder="customer-intent-analysis" />
            </Form.Item>

            <Form.Item
              name="display_name"
              label="展示名称（中文）"
              rules={[{ required: true, message: '请输入展示名称' }]}
            >
              <Input placeholder="客户意向分析" />
            </Form.Item>

            <Form.Item
              name="category"
              label="分类"
              rules={[{ required: true, message: '请选择分类' }]}
            >
              <Select
                options={[
                  { value: '客户管理', label: '客户管理' },
                  { value: '数据分析', label: '数据分析' },
                  { value: '营销工具', label: '营销工具' },
                  { value: '自动化', label: '自动化' },
                ]}
              />
            </Form.Item>

            <Form.Item
              name="description"
              label="功能描述"
              rules={[{ required: true, message: '请输入功能描述' }]}
            >
              <TextArea rows={4} placeholder="详细描述应用的功能和使用场景..." />
            </Form.Item>

            <Form.Item>
              <Button type="primary" htmlType="submit" size="large">
                下一步
              </Button>
            </Form.Item>
          </Form>
        </Card>
      )}

      {currentStep === 1 && (
        <Card title="第 2 步：上传代码包">
          <Form layout="vertical" onFinish={(values) => {}}>
            <Form.Item
              name="version"
              label="版本号"
              rules={[
                { required: true, message: '请输入版本号' },
                { pattern: /^\d+\.\d+\.\d+$/, message: '版本号格式：x.y.z' },
              ]}
            >
              <Input placeholder="1.0.0" />
            </Form.Item>

            <Form.Item name="changelog" label="更新日志">
              <TextArea rows={3} placeholder="描述本次更新的内容..." />
            </Form.Item>

            <Form.Item label="上传文件">
              <Dragger
                {...uploadProps}
                customRequest={({ file, onSuccess }: any) => {
                  form.validateFields(['version', 'changelog']).then((values) => {
                    handleFileUpload(file, values);
                    onSuccess('ok');
                  });
                }}
              >
                <p className="ant-upload-drag-icon">
                  <InboxOutlined />
                </p>
                <p className="ant-upload-text">点击或拖拽文件到此区域上传</p>
                <p className="ant-upload-hint">
                  仅支持 .zip 文件，大小限制 50MB
                  <br />
                  必须包含 manifest.json 文件
                </p>
              </Dragger>
            </Form.Item>

            {uploading && (
              <Progress
                percent={uploadProgress}
                status={uploadProgress === 100 ? 'success' : 'active'}
              />
            )}
          </Form>
        </Card>
      )}
    </div>
  );
};

export default PublishPage;
