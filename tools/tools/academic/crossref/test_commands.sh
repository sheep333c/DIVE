#!/bin/bash

# Crossref REST API 测试命令集
# 基于 Swagger 文档 v3.43.0

echo "=== Crossref REST API 测试命令 ==="
echo ""

# 基础配置
BASE_URL="https://api.crossref.org"
MAILTO="test@example.com"  # 建议使用真实邮箱以获得更好的服务

echo "1. 基础查询 - 获取前5个学术作品"
curl -s "${BASE_URL}/works?mailto=${MAILTO}&rows=5" | head -50
echo ""

echo "2. 按关键词搜索学术作品"
curl -s "${BASE_URL}/works?query=machine+learning&mailto=${MAILTO}&rows=3" | head -50
echo ""

echo "3. 按作者搜索"
curl -s "${BASE_URL}/works?query.author=einstein&mailto=${MAILTO}&rows=3" | head -50
echo ""

echo "4. 搜索特定期刊"
curl -s "${BASE_URL}/journals?query=nature&mailto=${MAILTO}&rows=3" | head -50
echo ""

echo "5. 获取特定DOI的详细信息"
curl -s "${BASE_URL}/works/10.1038/nature12373?mailto=${MAILTO}" | head -50
echo ""

echo "6. 按类型过滤（期刊文章）"
curl -s "${BASE_URL}/works?filter=type:journal-article&mailto=${MAILTO}&rows=3" | head -50
echo ""

echo "7. 按发表时间过滤（2023年）"
curl -s "${BASE_URL}/works?filter=from-pub-date:2023-01-01,until-pub-date:2023-12-31&mailto=${MAILTO}&rows=3" | head -50
echo ""

echo "8. 搜索有摘要的文章"
curl -s "${BASE_URL}/works?filter=has-abstract:1&mailto=${MAILTO}&rows=3" | head -50
echo ""

echo "9. 获取资助机构信息"
curl -s "${BASE_URL}/funders?query=national+science+foundation&mailto=${MAILTO}&rows=3" | head -50
echo ""

echo "10. 获取成员（出版商）信息"
curl -s "${BASE_URL}/members?query=springer&mailto=${MAILTO}&rows=3" | head -50
echo ""

echo "11. 按发表者和年份组合搜索"
curl -s "${BASE_URL}/works?query.publisher-name=nature&filter=from-pub-date:2022&mailto=${MAILTO}&rows=3" | head -50
echo ""

echo "12. 获取工作类型统计"
curl -s "${BASE_URL}/works?facet=type-name:10&mailto=${MAILTO}&rows=0" | head -50
echo ""

echo "13. 搜索开放获取文章"
curl -s "${BASE_URL}/works?filter=has-license:1&mailto=${MAILTO}&rows=3" | head -50
echo ""

echo "14. 按ORCID搜索作者"
curl -s "${BASE_URL}/works?filter=has-orcid:1&mailto=${MAILTO}&rows=3" | head -50
echo ""

echo "15. 选择特定字段返回"
curl -s "${BASE_URL}/works?select=DOI,title,author&mailto=${MAILTO}&rows=3" | head -50
echo ""

echo "=== 测试完成 ==="