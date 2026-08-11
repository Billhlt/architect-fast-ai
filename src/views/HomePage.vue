<template>
  <div class="navigation">
    <button @click="goToPageOne" class="nav-btn">前往页面一</button>
    <button @click="goToPageTwo" class="nav-btn">前往页面二</button>
  </div>
  <div class="container">
   <div class="wrapper">
    <div
      v-for="i in div_count"
      :key="i"
      class="box"
      :class="{ 'selected': selectedBoxes.includes(i-1) }"
    >
      <div class="text-content" v-html="processedTexts[i-1]" @mouseover="showTooltip" @mouseout="hideTooltip"></div>
       <div class="button-container">
         <button class="border-toggle" @click="toggleBoxBorder(i-1)">边框</button>
          <button class="image-toggle" @click="toggleImageTooltip($event, i-1)">图片</button>
         <button class="link-toggle" @click="openArticleLink(i-1)">链接</button>
       </div>
    </div>
   </div>
  </div>
  <p class="line">
    <span @mouseover="selectFirst">将鼠标放在这段文字</span>上，文字将会被自动选中。
  </p>

  <!-- 弹出文本框 -->
  <div v-if="tooltipVisible" class="tooltip" :style="tooltipStyle">
    {{ tooltipContent }}
  </div>

  <!-- 图片悬浮提示框 -->
  <div v-if="imageTooltipVisible" class="image-tooltip" :style="imageTooltipStyle" v-html="imageTooltipContent">
  </div>
</template>

<script setup>
import { getSummary, getPicsUrls} from '../services/api'
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter();

const goToPageOne = () => {
  router.push('/');
};

const goToPageTwo = () => {
  router.push('/page-two');
};


const div_count = ref(0)
const first = ref(null)
const userInput = ref('');
const messages = ref([]);
const valuez = ref([]);
const selectedBoxes = ref([]); // 跟踪被选中的box
const picsData = ref([]); // 存储图片数据




//############################以下为测试用例################################
// const set1 = ref(['中国稀土8月1日股价下跌3.12%，成交额18.44亿元。中美经贸会谈达成延长暂停加征关税措施90天的协议，并就中国稀土出口进行细化谈判。中国在全球稀土及永磁材料市场占据主导地位，这使其在贸易谈判中具有重要筹码。当前舆情以正面为主，占比68.4%。贸易关系缓和、稀土出口协议细化以及中国稀土市场主导地位等因素短期内可能对稀土股价产生积极影响，长期则取决于中美贸易关系的持续稳定。主要传播渠道为今日头条平台。'   ,'午休的电梯里，我独自上升。镜面墙映出四个我，像被切片的时间。13层按钮亮着，像颗不肯熄灭的星。'   ,'清理外婆的旧冰箱时，我在冷冻室发现一只冻成琥珀的知了。它翅膀上的脉络，像被封存的银河地图。'   ,'末班地铁像条疲惫的龙，驮着零星乘客滑进隧道。我对面的男人抱着纸箱，箱里探出一只奶猫的脑袋，琥珀色眼睛盯着我。'   ,'凌晨三点，便利店像座发光的孤岛。我蹲在冰柜前挑酸奶，忽然听见收银台传来"生日快乐"的旋律——店员正对着一块小蛋糕，给自己点蜡烛。'   ,'凌晨两点，便利店的日光灯管嗡嗡作响。我蹲在冰柜前挑速食饭团，发现最里面藏着一个过期三天的金枪鱼口味。'   ,'末班地铁像条喝醉的银龙，在隧道里东倒西歪。我对面的西装男正用领带擦眼镜，镜片下是哭肿的眼皮。'   ,'梧桐把整条街拧出绿色的水。我躲进"昨日书屋"时，店主正在用毛笔给一本《昆虫记》画插图，钢笔画的蚂蚁背着米粒大的米开朗琪罗雕像。'   ,'整理外婆遗物时发现本1998年的日历，六月份以后全是空白，直到12月31日突然出现她歪歪扭扭的字："今天小孙子说我的皱纹像葡萄干。'   ,'批发市场的灯管冻成青白色，番茄堆成火山，辣椒在编织袋里流血。戴雷锋帽的老汉把最后一把菠菜塞进我篮子："姑娘，这菜今早三点还在地里做梦。'   ,'大厦停电时，我和一个穿恐龙睡衣的男孩被困在17楼。他用手机光照亮电梯广告，突然指着某理财产品的秃头经理说："这是我爸。"', '123hahahahahah大厦停电时，我和一个穿恐龙睡衣的男孩被困在17楼。他用手机光照亮电梯广告，突然指着某理财产品的秃头经理说："这是我爸。"'])

// // 三维集合，表示要添加提示的字符位置（左闭右开区间），例：第一二个字的位置是[0, 2]，第四五个字的位置是[3, 5]
// const ranges = ref([[[12, 18], [3, 5], [10, 11]], [[1, 3], [4, 6], [11, 13]], [[2, 4], [5, 7], [12, 14]], [[3, 5], [6, 8], [13, 15]], [[4, 6], [7, 9], [14, 16]], [[5, 7], [8, 10], [15, 17]], [[6, 8], [9, 11], [16, 18]], [[7, 9], [10, 12], [17, 19]], [[8, 10], [11, 13], [18, 20]], [[9, 11], [12, 14], [19, 21]], [[10, 12], [13, 15], [20, 22]], [[11, 13], [14, 16], [20, 22]]]);

// // 添加提示信息数组
// const tooltipMessages = ref([['地铁末班车777', '雨天的旧书店77', '外婆的日历123'], ['地铁末班车778', '雨天的旧书店78', '外婆的日历124'], ['地铁末班车779', '雨天的旧书店79', '外婆的日历125'], ['地铁末班车780', '雨天的旧书店80', '外婆的日历126'], ['地铁末班车781', '雨天的旧书店81', '外婆的日历127'], ['地铁末班车782', '雨天的旧书店82', '外婆的日历128'], ['地铁末班车783', '雨天的旧书店83', '外婆的日历129'], ['地铁末班车784', '雨天的旧书店84', '外婆的日历130'], ['地铁末班车785', '雨天的旧书店85', '外婆的日历131'], ['地铁末班车786', '雨天的旧书店86', '外婆的日历132'], ['地铁末班车787', '雨天的旧书店87', '外婆的日历133'], ['地铁末班车779', '雨天的旧书店79', '外婆的日历125']]);
const ranges = ref([]);
const set1 = ref([]);
const tooltipMessages = ref([]);
onMounted(async () => {
  try {
    // const wordPositionResponse = await getWordPosition();
    // ranges.value = wordPositionResponse.data;

    const summaryResponse = await getSummary();
    set1.value = summaryResponse.data;
    div_count.value = set1.value.length;  // 添加这行来更新div_count

    // 获取图片数据
    const picsResponse = await getPicsUrls();
    picsData.value = picsResponse.data;
  } catch (error) {
    console.error('获取数据失败:', error);
  }
});






// 工具提示相关
const tooltipVisible = ref(false);
const tooltipContent = ref('');
const tooltipStyle = ref({
  position: 'absolute',
  zIndex: 1000,
  backgroundColor: '#333',
  color: '#fff',
  padding: '5px 10px',
  borderRadius: '4px',
  fontSize: '14px',
  maxWidth: '200px',
  wordWrap: 'break-word'
});

// 处理文本，为指定范围添加提示
const processedTexts = computed(() => {
  return set1.value.map((text, index) => {
    if (!ranges.value[index]) return text;

    let result = '';
    let lastEnd = 0;

    ranges.value[index].forEach((range, rangeIndex) => {
      // 添加范围前的文本
      result += text.substring(lastEnd, range[0]);

      // 添加带提示的文本
      const highlightedText = text.substring(range[0], range[1]);
      const tooltip = tooltipMessages.value[index] && tooltipMessages.value[index][rangeIndex]
        ? tooltipMessages.value[index][rangeIndex]
        : '提示信息';

      result += `<span class="tooltip-trigger" data-tooltip="${tooltip}">${highlightedText}</span>`;

      lastEnd = range[1];
    });

    // 添加剩余文本
    result += text.substring(lastEnd);

    return result;
  });
});

// 显示提示
const showTooltip = (event) => {
  const target = event.target;
  if (target.classList.contains('tooltip-trigger')) {
    tooltipContent.value = target.getAttribute('data-tooltip');
    tooltipStyle.value = {
      ...tooltipStyle.value,
      left: `${event.pageX + 10}px`,
      top: `${event.pageY + 10}px`
    };
    tooltipVisible.value = true;
  }
};

// 隐藏提示
const hideTooltip = () => {
  tooltipVisible.value = false;
};

// 图片悬浮提示相关
const imageTooltipVisible = ref(false);
const imageTooltipContent = ref('');
const imageTooltipStyle = ref({
  position: 'absolute',
  zIndex: 1000,
  backgroundColor: '#333',
  color: '#fff',
  padding: '10px 15px',
  borderRadius: '4px',
  fontSize: '16px',
  maxWidth: '90vw', // 改为视窗宽度的90%，确保不会超出屏幕
  wordWrap: 'break-word'
});

// 切换图片提示框显示状态
const toggleImageTooltip = (event, index) => {
  // 如果提示框已显示，则隐藏它
  if (imageTooltipVisible.value) {
    imageTooltipVisible.value = false;
    return;
  }

  // 获取对应索引的图片链接列表
  const pics = picsData.value[index] || [];

  // 生成图片HTML - 使用自适应列布局
  let imagesHtml = '';
  if (pics.length > 0) {
    // 根据图片数量自动调整列数，确保在小屏幕上也能正常显示
    const columns = Math.min(pics.length, 3);
    // 增加最小宽度，确保图片不会太小
    imagesHtml = `<div style="display: grid; grid-template-columns: repeat(${columns}, minmax(500px, 1fr)); gap: 30px; width: 100%;">`;
    // 使用响应式图片尺寸，确保图片不会超出容器，但保证最小高度
    imagesHtml += pics.map(url => `<img src="${url}" style="width: 100%; height: auto; min-height: 400px; max-height: 700px; object-fit: cover; border-radius: 8px;" />`).join('');
    imagesHtml += `</div>`;
  } else {
    imagesHtml = '暂无图片';
  }

  // 设置图片内容
  imageTooltipContent.value = imagesHtml;

  // 获取视窗尺寸
  const viewportWidth = window.innerWidth;
  const viewportHeight = window.innerHeight;

  // 获取按钮元素的位置和尺寸
  const buttonRect = event.target.getBoundingClientRect();

  // 计算提示框的实际宽高（基于内容）
  const tooltipWidth = Math.min(1800, viewportWidth * 0.9); // 最大宽度为视窗宽度的90%
  const tooltipHeight = Math.min(1000, viewportHeight * 0.8); // 最大高度为视窗高度的80%

  // 计算初始位置
  let left = buttonRect.left + 10;
  let top = buttonRect.bottom + 10;

  // 判断按钮是否在右侧区域（屏幕右半部分）
  const isRightSide = buttonRect.left > viewportWidth / 2;

  // 如果按钮在右侧，将提示框显示在按钮左侧
  if (isRightSide) {
    left = buttonRect.left - tooltipWidth - 10;
    // 确保左侧不会超出屏幕边界
    if (left < 10) {
      left = 10;
    }
  }

  // 调整位置，确保提示框不会超出屏幕底部
  if (top + tooltipHeight > viewportHeight) {
    // 显示在按钮上方
    top = buttonRect.top - tooltipHeight - 10;

    // 如果上方空间也不足，则显示在屏幕中间位置
    if (top < 10) {
      top = viewportHeight / 2 - tooltipHeight / 2;
    }
  }

  // 确保不会超出屏幕右边界（当按钮在左侧时）
  if (!isRightSide && left + tooltipWidth > viewportWidth) {
    left = viewportWidth - tooltipWidth - 10;
  }

  // 确保不会超出屏幕左边界和顶部
  left = Math.max(10, left);
  top = Math.max(10, top);

  // 设置提示框位置
  imageTooltipStyle.value = {
    ...imageTooltipStyle.value,
    left: `${left}px`,
    top: `${top}px`,
    width: `${tooltipWidth}px`,
    maxHeight: `${tooltipHeight}px`
  };

  imageTooltipVisible.value = true;
};

// 隐藏图片提示（保留此函数，以便在其他地方调用）
const hideImageTooltip = () => {
  imageTooltipVisible.value = false;
};

// 添加点击外部关闭提示框的功能
document.addEventListener('click', function(event) {
  const imageTooltip = document.querySelector('.image-tooltip');
  const imageButton = event.target.closest('.image-toggle');

  // 如果点击的不是图片按钮且提示框是显示状态，且点击的不是提示框内部，则关闭提示框
  if (imageTooltip && imageTooltipVisible.value && !imageButton && !imageTooltip.contains(event.target)) {
    imageTooltipVisible.value = false;
  }
});

// 其他功能函数
const selectFirst = () => {
  const textElement = document.querySelector('.line span');
  if (textElement) {
    const range = document.createRange();
    range.selectNodeContents(textElement);
    const selection = window.getSelection();
    selection.removeAllRanges();
    selection.addRange(range);
  }
};

const toggleBoxBorder = (index) => {
  if (selectedBoxes.value.includes(index)) {
    selectedBoxes.value = selectedBoxes.value.filter(i => i !== index);
  } else {
    selectedBoxes.value.push(index);
  }
};

const openArticleLink = (index) => {
  // 从文本中提取链接，链接通常在文本末尾，以"文章链接为："开头
  const text = set1.value[index];
  if (!text) return;

  // 查找链接
  const linkPattern = /文章链接为：(.+)/;
  const match = text.match(linkPattern);

  if (match && match[1]) {
    // 提取链接并去除可能的空白字符
    const link = match[1].trim();
    // 在新窗口中打开链接
    window.open(link, "_blank");
  }
};
</script>

<style scoped>
.navigation {
  display: flex;
  justify-content: center;
  padding: 20px;
}

.nav-btn {
  margin: 0 10px;
  padding: 8px 16px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.wrapper {
  display: grid;
  grid-template-columns: repeat(4, minmax(550px, 1fr));
  gap: 20px;
  max-width: 3000px;
  margin: 0 auto;
  padding: 0 20px;
  justify-content: center;
}

.box {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 15px;
  background-color: #f9f9f9;
  transition: all 0.3s ease;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  height: 350px;
}

.box:hover {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.box.selected {
  border: 2px solid #4CAF50;
  background-color: #d4f5b0;
}

.text-content {
  margin-bottom: 10px;
  line-height: 1.5;
  word-wrap: break-word;
  overflow-wrap: break-word;
  white-space: pre-wrap;
  max-width: 100%;
  box-sizing: border-box;
  flex-grow: 1;
  overflow-y: auto;
  font-size: 20px;
  padding-right: 5px;
}

.tooltip-trigger {
  background-color: #ffeb3b;
  cursor: pointer;
  position: relative;
}

.button-container {
  display: flex;
  justify-content: space-between;
}

.border-toggle, .link-toggle, .image-toggle {
  padding: 8px 15px;
  background-color: #2196F3;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
}

.image-toggle {
  background-color: #b370c7;
}

.image-tooltip {
  position: absolute;
  z-index: 1000;
  background-color: #333;
  color: #fff;
  padding: 30px 40px;
  border-radius: 16px;
  font-size: 36px;
  max-width: 95vw; /* 改为视窗宽度的95%，确保不会超出屏幕 */
  max-height: 90vh; /* 限制最大高度为视窗高度的90% */
  overflow-y: auto; /* 内容超出时允许滚动 */
  word-wrap: break-word;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
}

.line {
  margin-top: 30px;
  text-align: center;
}

.line span {
  cursor: pointer;
  font-weight: bold;
}

.tooltip {
  position: absolute;
  z-index: 1000;
  background-color: '#333';
  color: '#fff';
  padding: '5px 10px';
  borderRadius: '4px';
  fontSize: '14px';
  maxWidth: '200px';
  wordWrap: 'break-word';
}
</style>