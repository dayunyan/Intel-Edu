import React from 'react';
import { Tree, Card } from 'antd';
import type { DataNode } from 'antd/es/tree';

interface CurriculumProps {
  subject: string;
  loading?: boolean;
  subjectId: number;
}

const CurriculumTree: React.FC<CurriculumProps> = ({ subject }) => {
  const treeData: DataNode[] = [
    {
      title: subject,
      key: '0',
      children: [
        {
          title: '教材一',
          key: '0-0',
          children: [
            {
              title: '第一章',
              key: '0-0-0',
              children: [
                { title: '第一节', key: '0-0-0-0' },
                { title: '第二节', key: '0-0-0-1' },
              ],
            },
            {
              title: '第二章',
              key: '0-0-1',
              children: [
                { title: '第一节', key: '0-0-1-0' },
                { title: '第二节', key: '0-0-1-1' },
              ],
            },
          ],
        },
      ],
    },
  ];

  return (
    <Card title={`${subject}课程内容`} className="m-4">
      <Tree
        showLine
        defaultExpandAll
        treeData={treeData}
        className="bg-white p-4"
      />
    </Card>
  );
};

export default CurriculumTree; 