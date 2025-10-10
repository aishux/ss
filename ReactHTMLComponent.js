import rehypeRaw from "rehype-raw";

   <ReactMarkdown
      className={`${styles.formattedtext} ${
        smallscreen && !smallscreenExpanded ? styles.smallcontainer : ""
      }`}
      children={answerHtml}
      remarkPlugins={[remarkGfm, remarkMath]}
      rehypePlugins={[
        rehypeRaw,
        rehypeKatex,
      ]}
      components={{
        table: renderTable,
        code: renderCode,
        a: renderLink,
      }}
    />
  );
}
