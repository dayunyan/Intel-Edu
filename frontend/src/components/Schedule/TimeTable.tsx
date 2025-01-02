import React from 'react';
import { Table, Spin } from 'antd';
import type { ColumnsType } from 'antd/es/table';
import type { Class } from '@/types/curriculum';

interface TimeTableProps {
  loading: boolean;
  data: Class[];
}

interface TimeSlot {
  time: string;
  [key: string]: string;
}

const TimeTable: React.FC<TimeTableProps> = ({ loading, data }) => {
  const columns: ColumnsType<TimeSlot> = [
    { title: '时间', dataIndex: 'time', key: 'time', width: 100 },
    { title: '周一', dataIndex: 'monday', key: 'monday' },
    { title: '周二', dataIndex: 'tuesday', key: 'tuesday' },
    { title: '周三', dataIndex: 'wednesday', key: 'wednesday' },
    { title: '周四', dataIndex: 'thursday', key: 'thursday' },
    { title: '周五', dataIndex: 'friday', key: 'friday' },
  ];

  const formatTime = (time: string) => {
    // 确保时间格式为两位数
    return time.split(':').map(t => t.padStart(2, '0')).join(':');
  };

  const formatScheduleData = (classes: Class[]): TimeSlot[] => {
    // 将API返回的数据转换为表格所需的格式
    const timeSlots: TimeSlot[] = [
      { time: '08:00:00-09:40:00' },
      { time: '10:00:00-11:40:00' },
      { time: '14:00:00-15:40:00' },
      { time: '16:00:00-17:40:00' },
    ];

    classes.forEach(classItem => {
      const dayMap: { [key: string]: string } = {
        '1': 'monday',
        '2': 'tuesday',
        '3': 'wednesday',
        '4': 'thursday',
        '5': 'friday',
      };
      
      const formattedStartTime = formatTime(classItem.start_time);
      const formattedEndTime = formatTime(classItem.end_time);
      const timeString = `${formattedStartTime}-${formattedEndTime}`;
      
      const timeIndex = timeSlots.findIndex(slot => slot.time === timeString);
      console.log('Class Item:', classItem);
      console.log('Formatted Time:', timeString);
      console.log('Time Index:', timeIndex);
      
      if (timeIndex !== -1) {
        const date = new Date(classItem.date);
        const day = date.getDay().toString();
        console.log('Date:', classItem.date);
        console.log('Day:', day);
        
        if (day in dayMap) {
          timeSlots[timeIndex][dayMap[day]] = `${classItem.name}\n${classItem.teacher_name}`;
        }
      }
    });

    return timeSlots;
  };

  return (
    <div className="p-4"> 
      <Spin spinning={loading}> 
        <Table 
          columns={columns} 
          dataSource={formatScheduleData(data)} 
          pagination={false}
          bordered
          className="shadow-lg"
        />
      </Spin>
    </div>
  );
};

export default TimeTable; 