// ==UserScript==
// @name         dy
// @namespace    http://tampermonkey.net/
// @version      2025-04-05
// @description  try to take over the world!
// @author       You
// @match        https://www.douyin.com/user/self*
// @icon         https://www.google.com/s2/favicons?sz=64&domain=douyin.com
// @grant        none
// ==/UserScript==

(function() {
    'use strict';

// 导入axios.pos
let script = document.createElement('script');
//script.src = "https://cdn.jsdelivr.net/npm/axios/dist/axios.min.js";
    script.src = "https://unpkg.com/axios@1.8.4/dist/axios.min.js";
document.getElementsByTagName('head')[0].appendChild(script);

function get_url() {

// 定义接收请求的URL常量
const RECEIVER_URL = 'http://127.0.0.1:9090/download';

// 检查URL是否包含 'post' 或 'video'
function good_url(url) {
    // 如果URL包含 'post' 或 'video'，则返回该URL，否则返回 null
    return url.includes('post') || url.includes('video') ? url : null;
}

// 发送URL到指定的接收地址
function send(url) {
    axios.post(RECEIVER_URL, {
        url: url
    })
   .then((res) => {
        // 打印响应状态码
        console.log(res.status);
    })
   .catch((error) => {
        // 打印请求失败的错误信息
        console.error('Error sending URL:', error);
    });
}

// 重写 window.fetch 方法，检测符合条件的请求并发送URL
(function() {
    // 保存原始的 window.fetch 方法
    const originalFetch = window.fetch;
    window.fetch = function(url, init) {
        // 检查URL是否符合条件
        const validUrl = good_url(url);
        if (validUrl) {
            // 发送符合条件的URL
          send(validUrl);
          console.log(validUrl)
            // 打印检测到的请求URL
            console.log('Fetch request to:', url);
        }
        // 调用原始的 fetch 方法
        return originalFetch.apply(this, arguments);
    };
})();
}

get_url()


function send2(data,url){

}


function formatBytes(bytes) {
    const units = ['B', 'KB', 'MB', 'GB', 'TB'];
    let unitIndex = 0;
    let size = bytes;

    while (size >= 1024 && unitIndex < units.length - 1) {
        size /= 1024;
        unitIndex++;
    }

    // 保留两位小数
    const formattedSize = parseFloat(size.toFixed(1));
    return `${formattedSize} ${units[unitIndex]}`;
}

function processLikes(like) {
    if (typeof like === 'string' && like.includes('万')) {
        like = like.replace('万', '');
        like = Math.floor(parseFloat(like) * 10000);
    }
    return parseInt(like, 10);
}

function generateFilename(data) {
    // 提取作者名
    const author = data.desc.split('\n')[0].replace('@', '');

    // 提取年月和日用字母表顺序表示
    const date = new Date(data.now);
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String.fromCharCode(96 + date.getDate());
    const likes_raw=data.stat.split('\n')[0]
    // 提取点赞数据并转换为二进制
    const likes = formatBytes(processLikes(likes_raw), 10)

    // 提取描述的后部
    const descRear = data.desc.split('\n').slice(2).join(' ');

    // 生成文件名
    const filename = `${author} ${year}-${month}${day} ${likes} ${descRear}.mp4`;
    return filename;
}

const data = {
    "stat": "7692\n135\n755\n1810\n看相关",
    "id": "7495329378935967011",
    "desc": "@高原\n· 3小时前\n正装大光明的魅力 #氛围感 #御姐 #高级感 #美出高级感 #清冷感",
    "reply": "",
    "now": "2025-4-20 21:09:05"
};
class DySender {
  constructor() {
    this.old = null;
    this.interval = null;
  }



  dyInfo() {
    let getDyOne=(info)=>{return info.length === 3 ? info[1] : info[0];}
    const dy = {};
    dy.stat = document.querySelectorAll("div[data-state='normal']")[3].nextSibling.innerText
    const info = getDyOne(document.querySelectorAll('.video-info-detail'));
    dy.id = info.dataset.e2eAwemeId;
    dy.desc = info.innerText;

    // dy.reply =  document.querySelector('#relatedVideoCard').innerText;
    dy.reply =  "";
    dy.now = new Date().toLocaleString().replaceAll('/', '-');
     dy.file_name=generateFilename(dy)
    return dy;
  }

  sendDy() {
    const dy = this.dyInfo();
    if (this.old && this.old.id === dy.id) {
      return 'skip';
    }
    console.log(dy)
    axios.post('http://127.0.0.1:9090/save', {
      url: window.location.href,
      data: dy,
    }).then(
      (res)=>{
        console.log(res.status)
        console.log('success '+dy.desc)
      }
    );
    this.old = dy;
  }

  startSending() {
    this.interval = setInterval(() => {
      this.sendDy();
    }, 300);
  }

  stopSending() {
    clearInterval(this.interval);
  }
}

const dySender = new DySender();
dySender.startSending();








css_click = 'body > main > div.content-container.container.relative.my-11 > div.flex.flex-col > div > button'

function click_dy() {
  eles = document.querySelectorAll(".xgplayer-playswitch-next")
  if (eles.length > 1)
    eles[1].click()
}

function click_cs() {
  document.querySelectorAll("div[data-e2e='video-switch-next-arrow']")[1].click()
}
function space_click() {
  let wait=2000
  let intervalId = null; // 存储定时器ID
  let isLooping = false; // 状态标记


document.addEventListener('keydown', function(event) {
  // 检测空格键（兼容新旧浏览器）
  if (event.code === 'Space' || event.keyCode === 32) {
    event.preventDefault(); // 阻止默认滚动行为[1,6](@ref)

    if (!isLooping) {
      // 启动循环点击
      intervalId = setInterval(() => {
       click_cs()
        console.log('循环点击中...');
      }, wait); // 间隔500ms（可调整）
      isLooping = true;
    } else {
      // 停止循环
      clearInterval(intervalId);
      isLooping = false;
      console.log('已停止循环');
    }
  }
});
}

space_click()

 console.log('run...')

// document.querySelector('div[data-e2e="user-detail"]').addEventListener('dblclick',()=> alert(1) )
    // Your code here...
})();