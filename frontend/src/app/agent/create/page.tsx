'use client';

import { useState } from 'react';
import { Form, Input, Button, Upload, message } from 'antd';
import { CameraOutlined } from '@ant-design/icons';
import { agentApi } from '@/services/agent';
import { useRouter } from 'next/navigation';
import type { UploadFile } from 'antd/es/upload/interface';
import { RcFile } from 'antd/es/upload';

export default function CreateAgentPage() {
  const [form] = Form.useForm();
  const router = useRouter();
  const [avatarFile, setAvatarFile] = useState<UploadFile | null>(null);

  const onFinish = async (values: any) => {
    try {
      const formData = new FormData();
      formData.append('student_id', localStorage.getItem('userId') || '');
      formData.append('name', values.name);
      formData.append('description', values.description);
      if (avatarFile?.originFileObj) {
        formData.append('avatar', avatarFile.originFileObj);
      }

      await agentApi.createAgent(formData);
      message.success('创建成功');
      router.push('/chat');
    } catch (error) {
      message.error('创建失败');
    }
  };

  const beforeUpload = (file: RcFile) => {
    const isImage = file.type.startsWith('image/');
    if (!isImage) {
      message.error('只能上传图片文件！');
      return false;
    }

    const isLt2M = file.size / 1024 / 1024 < 2;
    if (!isLt2M) {
      message.error('图片必须小于2MB！');
      return false;
    }

    // 创建一个新的 FileReader
    const reader = new FileReader();
    reader.onload = (e) => {
      const img = new Image();
      img.onload = () => {
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');
        
        // 设置画布大小为目标尺寸
        canvas.width = 200;
        canvas.height = 200;
        
        // 计算裁剪区域
        const size = Math.min(img.width, img.height);
        const x = (img.width - size) / 2;
        const y = (img.height - size) / 2;
        
        // 绘制裁剪后的图像
        ctx?.drawImage(
          img,
          x, y, size, size,  // 源图像裁剪
          0, 0, 200, 200     // 目标尺寸
        );
        
        // 转换为Blob
        canvas.toBlob((blob) => {
          if (blob) {
            const newFile = new File([blob], file.name, {
              type: 'image/jpeg',
            });
            setAvatarFile({
              uid: '-1',
              name: file.name,
              status: 'done',
              url: URL.createObjectURL(blob),
              originFileObj: newFile as RcFile
            });
          }
        }, 'image/jpeg', 0.9);
      };
      img.src = e.target?.result as string;
    };
    reader.readAsDataURL(file);

    return false; // 阻止默认上传行为
  };

  return (
    <div style={{ 
      maxWidth: '400px', 
      margin: '40px auto', 
      padding: '20px',
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center'
    }}>
      <Upload
        listType="picture-circle"
        showUploadList={false}
        beforeUpload={beforeUpload}
      >
        {avatarFile ? (
          <img 
            src={avatarFile.url} 
            alt="avatar" 
            style={{ 
              width: '100%', 
              height: '100%', 
              borderRadius: '50%',
              objectFit: 'cover' 
            }} 
          />
        ) : (
          <div>
            <CameraOutlined style={{ fontSize: '24px', color: '#666' }} />
          </div>
        )}
      </Upload>

      <Form
        form={form}
        layout="vertical"
        style={{ width: '100%' }}
        onFinish={onFinish}
      >
        <Form.Item
          name="name"
          rules={[{ required: true, message: '请输入智能体名称' }]}
        >
          <Input placeholder="智能体名称" />
        </Form.Item>

        <Form.Item
          name="description"
          rules={[{ required: true, message: '请输入智能体描述' }]}
        >
          <Input.TextArea 
            placeholder="描述智能体的角色、语气、性格等" 
            rows={4}
          />
        </Form.Item>

        <Form.Item style={{ marginTop: '24px' }}>
          <div style={{ display: 'flex', gap: '12px', justifyContent: 'center' }}>
            <Button 
              danger 
              onClick={() => router.back()}
              style={{ width: '120px' }}
            >
              取消
            </Button>
            <Button 
              type="primary" 
              htmlType="submit"
              style={{ width: '120px' }}
            >
              确定
            </Button>
          </div>
        </Form.Item>
      </Form>
    </div>
  );
} 