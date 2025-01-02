module.exports = {
  // config options here
  images: {
    unoptimized: false,  // 如果不需要Next.js对图片进行优化，可以设置为true，可根据实际需求决定是否添加这行
    loader: 'default',
    path: '',  // 设置为空字符串，这样相对路径就可以直接写文件名等形式，而不用以 / 开头了
},
};
