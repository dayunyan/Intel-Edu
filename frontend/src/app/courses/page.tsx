'use client';

import { useEffect, useState } from 'react';
import { Tabs, message } from 'antd';
import TimeTable from '@/components/Schedule/TimeTable';
import CurriculumTree from '@/components/Curriculum/CurriculumTree';
import { curriculum } from '@/services/api';
import type { Subject, Class } from '@/types/curriculum';

const { TabPane } = Tabs;

export default function CoursesPage() {
  const [loading, setLoading] = useState(true);
  const [subjects, setSubjects] = useState<Subject[]>([]);
  const [schedule, setSchedule] = useState<Class[]>([]);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [subjectsResponse, scheduleResponse] = await Promise.all([
        curriculum.getSubjects(),
        curriculum.getSchedule()
      ]);
      
      console.log('Schedule Response:', scheduleResponse.data);
      setSubjects(subjectsResponse.data);
      setSchedule(scheduleResponse.data);
    } catch (error) {
      console.error('Error fetching data:', error);
      message.error('获取课程数据失败');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mx-auto p-4">
      <h2 className="text-2xl font-bold mb-6">课程管理</h2>
      <Tabs defaultActiveKey="schedule">
        <TabPane tab="课程表" key="schedule">
          <TimeTable loading={loading} data={schedule} />
        </TabPane>
        <TabPane tab="课程内容" key="curriculum">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {subjects.map((subject) => (
              <CurriculumTree 
                key={subject.id} 
                subject={subject.name}
                loading={loading}
                subjectId={subject.id}
              />
            ))}
          </div>
        </TabPane>
      </Tabs>
    </div>
  );
} 