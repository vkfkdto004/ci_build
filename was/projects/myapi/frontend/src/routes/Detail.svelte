<script>
    import fastapi from "D:/dev/projects/myapi/frontend/src/lib/api"

    export let params = {}
    let question_id = params.question_id
    let question = {}
    let content = ""

    function get_question() {
        fastapi("get", "/api/question/detail/" + question_id, {}, (json) => {
            question = json
        })
    }

    function post_answer() {
        // event.preventDefault()로 인하여 form이 자동으로 전송되는 것을 방지해줌
        event.preventDefault()
        let url= "/api/answer/create/" + question_id
        let params = {
            content: content
        }
        // 답변 등록이 성공하면 등록 답변이 textarea에서 지워지고(content=''), 상세화면에 새로운 결과값을 반영하기 위해서 get_question() 함수 실행 
        fastapi("post", url, params, (json) => {
            content= ''
            get_question()
        })
    }

    get_question()
</script>

<h1>{question.subject}</h1>
<div>
    {question.content}
</div>
<!--답변 등록을 위한 form 엘리먼트 추가-->
<form method="post">
    <!--textarea에 답변을 적고 아래 "답변등록" 버튼을 누르면 답변 등록. <script> 영역의 content와 연결되도록 bind:value={content} 속성 사용
    textarea에 값을 추가하거나 변경할 때 마다 content 값도 자동으로 변경-->
    <textarea rows="15" bind:value={content}></textarea>
    <input type="submit" value="답변등록" on:click="{post_answer}">
    <!-- 클릭 시 post_answer 함수 호출. textarea에 작성한 content를 파라미터로 답변 등록 API를 호출-->
</form>