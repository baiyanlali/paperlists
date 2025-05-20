import json
import re
from collections import Counter
import os
def load_papers(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def search_papers(papers, query):
    pattern = re.compile(re.escape(query), re.IGNORECASE)
    results = []
    for paper in papers:
        title = paper.get('title', '')
        keywords = ' '.join(paper.get('keywords', []))
        abstract = paper.get('abstract', '')
        if pattern.search(title) or pattern.search(keywords) or pattern.search(abstract):
            results.append(paper)
    return results

def papers_to_markdown_table(papers):
    # 统计 status 数量
    status_counter = Counter()
    keywords_counter = Counter()
    for paper in papers:
        status = paper.get('status', '')
        status_counter[status] += 1
        kw = paper.get('keywords', "")
        keywords_counter[kw] += 1

    # 构建统计信息的 markdown
    status_md = "### 录取状态统计\n"
    for k, v in status_counter.items():
        status_md += f"- {k}: {v}\n"
    keywords_md = "### 关键词统计\n"
    for k, v in keywords_counter.most_common():
        keywords_md += f"- {k}: {v}\n"

    header = "| 序号 | 标题 | 作者 | 关键词 | 录取状态 |\n|---|---|---|---|---|"
    rows = []
    for idx, paper in enumerate(papers, 1):
        title = paper.get('title', '').replace('\n', ' ')
        authors = paper.get('author_site', "")
        keywords = paper.get('keywords', "")
        status = paper.get('status', '')
        rows.append(f"| {idx} | {title} | {authors} | {keywords} | {status} |")
    return status_md + '\n' + '\n' + header + '\n' + '\n'.join(rows)

if __name__ == "__main__":
    os.makedirs("./survey", exist_ok=True)  # 创建输出目录
    # 修改为你的json文件路径
    json_path = "./iclr/iclr2025.json"
    
    papers = load_papers(json_path)
    queries = ["multi-modal", "content", "content generation", "generation", "procedural", "virtual reality", "mixed reality"]
    for query in queries:
    # query = "multi-modal"  # 修改为你的查询关键词
        results = search_papers(papers, query)
        if results:
            # print(papers_to_markdown_table(results))
            # 保存结果到以query命名的markdown文件
            safe_query = query.replace(' ', '_')
            output_path = f"./survey/{safe_query}.md"
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(papers_to_markdown_table(results))
            print(f"已保存结果到 {output_path}")
        else:
            print("未找到相关论文。")
