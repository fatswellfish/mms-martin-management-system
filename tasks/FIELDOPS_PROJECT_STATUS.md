# FieldOps 项目进度文档
版本：2026-02

## 一、当前状态（2026/02）

FieldOps 独立系统已建立
目录：mms/FieldOps/
包含：
- main.py
- router.py
- router_views.py
- router_rewrite.py
- router_api（待进一步完善）
- views/
- static/
- schemas/
- services/
- models/

### HTML 模板迁移成功
所有 legacy farm_domain 和 field_ops 下的 HTML 已复制到：
- mms/FieldOps/views/farm_domain/
- mms/FieldOps/views/field_ops/components/
- mms/FieldOps/views/field_ops/pages/

### 静态资源加载成功
- /static/css/style.css 正常工作

### UI 主页面可用
FieldOps 首页（Dashboard）已加载成功
Farm Tree、Batch Detail、Event Trace、Inbound Wizard 页面可渲染

### URL 重写器已生效
- /pig-farm/* → 自动跳转到 /FieldOps/*

### Jinja Loader 已修复
- farm/* include 已正确重写到 views/farm_domain

## 二、后端 API 进度
- **Tree API**：规划完成，模型结构已获取
- **Batch API**：未生成
- **Pen API**：未生成
- **Barn API**：未生成
- **Event API**：未生成
- **Experiment API**：未生成

## 三、待办工作
1. 基于 PigBatchLocation 重建 Tree API（下一阶段）
2. 生成 Barn/Pen/Batch/Event 的 models + services + API
3. 完成卡片 UI 的动态数据绑定
4. 实现事件滚动 EventScroller API
5. 实现免疫/实验方案 API

## 四、实例配置说明
- **产房**：共7舍，每个舍16栏，装猪只装15个，每栏15~16头猪，其中一个栏预留作为治疗、疗养用；
- **保育**：共6舍，一个舍16栏，每栏18~20头猪；
- **育肥**：共7舍，15舍叫育肥舍，一个舍12圈，一栏20头猪，其中10栏装猪，2栏预留作为留观疗养；
- **二保育**：6舍7舍叫二保育，每个舍12栏，一个栏30个猪，10栏装猪，2栏不装，也是预留作为治疗栏；
- **当前状态**：目前的600头，在保育的5舍、6舍，一栏20头，共600头；
- **今日计划**：今天下午转至二保育，6舍、7舍，一舍300头。
- **未来进猪**：预计下2月2日至8日之间进1500头，12月13日进1500头，不是之前的2200头了；
- **免疫计划**：这些猪预计进行一免，其中200~400头在销售最终会留下来，进行留种或育肥，留下来的猪做2免；
- **疫苗方案**：
  - **方案A**：疫苗足够 → 全部按计划进行（一免 + 二免）
  - **方案B**：疫苗不足 → 在保证600头二免的情况下，一部分猪不做1免，直接作为对照组出售；
  - **方案C**：疫苗更少 → 全部只做1免，不做2免；
  - 疫苗实际生产数量可能为：2900头份、3600头份或5000头份。