<script lang="ts">
	import "./app.css";
	import Header from "./components/Header.svelte";
	import { Backend, type SearchResponse, type TaxonomyInfo } from "./backend";
	import { onMount } from "svelte";
	import { Button, Textarea } from "flowbite-svelte";
	import {
		ArrowUpRightFromSquareOutline,
	} from "flowbite-svelte-icons";
	import Select from "svelte-select";

	let sequence = `MMITFQCLIGILLIANNLAFDICKASNPRFCKCQSHSKMQCGSFEVTTNTINNLIIKCSMKSDVNEISKIFLNVIEGENIDTAEVILENCLIVHDFNWYLPIFIVSGRELPFWLTISKRYEVYLYYLRAIETLESLTLSMINTLVIGSKAFDINPYLKTLRIKNNNFVKLDAKNPFWGLHNLEILEISKNKKVVFGREPFFLLPKLKILYLDNNNLESIPDKLFFGLDSLTDLVLSGNRIKSLTDESFFGLIMSLKRIDLKGNRLQKTEIDKIHKYFGDEFILIDY`;
	let topK = 100;
	let results: SearchResponse;
	let searchTimeMs: number;

	type SelectItem = { value: string; label: string; taxonomy: string };
	let items: SelectItem[] = [];
	let selectedFilters: SelectItem[] | undefined;

	$: isSequenceValid = validSequence(sequence);

	async function updateSearch(
		sequence: string,
		topK: number,
		selectedFilters: SelectItem[] | undefined
	) {
		let classFilters, phylumFilters;
		if (selectedFilters) {
			classFilters = selectedFilters
				.filter((d) => d.taxonomy === "class")
				.map((d) => d.value);
			phylumFilters = selectedFilters
				.filter((d) => d.taxonomy === "phylum")
				.map((d) => d.value);

			// don't filter if there are no filters, duh!
			if (classFilters.length === 0) classFilters = undefined;
			if (phylumFilters.length === 0) phylumFilters = undefined;
		}

		console.log(classFilters, phylumFilters);

		const startTime = performance.now();
		results = await Backend.computeSimilarity({
			sequence: sequence.toUpperCase(),
			topK,
			classFilters,
			phylumFilters,
		});
		const endTime = performance.now();
		searchTimeMs = endTime - startTime;
	}

	onMount(async () => {
		await updateSearch(sequence, topK, selectedFilters);

		const taxonomyInfo = await Backend.taxonomyInfo();
		items = parseTax(taxonomyInfo);
	});

	function validSequence(s: string) {
		if (s.length === 0) return false;

		const l = s.toUpperCase();
		const validAA = new Set("*ACDEFGHIKLMNPQRSTVWY");
		return Array.from(l).every((d) => validAA.has(d));
	}

	function parseTax(t: TaxonomyInfo) {
		const label = (categeory: string, item: string) =>
			`${item} [${categeory}]`;
		const classesItems = t.classes.map((d) => ({
			value: d,
			label: label("class", d),
			taxonomy: "class",
		}));
		const phylumItems = t.phyla.map((d) => ({
			value: d,
			label: label("phylum", d),
			taxonomy: "phylum",
		}));
		return classesItems.concat(phylumItems);
	}
</script>

<Header />

<main class="p-5">
	<div class="mb-10">
		<div class="mb-2">
			<b>Protein Sequence</b> (input/query)
		</div>
		<Textarea bind:value={sequence} rows={4} />
		<div class="mt-2 mb-4">
			<div class="mb-2">
				<b>Filter</b>
			</div>
			<div style="">
				<Select
					{items}
					placeholder="Filter by Class or Phylum"
					multiple
					bind:value={selectedFilters}
				/>
			</div>
		</div>
		<Button
			color="dark"
			disabled={!isSequenceValid}
			on:click={async () => {
				topK = 100;
				await updateSearch(sequence, topK, selectedFilters);
			}}
		>
			{#if isSequenceValid}
				Query 569k Database
			{:else}
				Enter valid residues
			{/if}
		</Button>
	</div>
	{#if results}
		<div class="mb-5" style="color: grey;">
			<b>{results.total}</b> results found in <b>{searchTimeMs.toFixed(0)}</b> ms
		</div>
		<div class="flex gap-5 flex-wrap">
			{#each results.hits as hit}
				<div class="protein">
					<div>
						<div class="title flex flex-col">
							<div class="flex flex-row">
							<Button
								size="xs"
								href="https://www.uniprot.org/uniprotkb/{hit.accession}/entry"
								target="_blank"
								outline
								>
								{hit.accession}
								<ArrowUpRightFromSquareOutline
									size="xs"
									class="ml-1"
								/>
							</Button>
						</div>
							{hit.proteinName}
						</div>
						<div style="color: grey">
							<div><b>Organism:</b> {hit.organismName}</div>
							<div><b>Class:</b> {hit.ncbiTaxonomyClass ?? "-"}</div>
							<div><b>Phylum:</b> {hit.ncbiTaxonomyPhylum ?? "-"}</div>
							<div>
								<b>Sequence Length:</b>
								{hit.sequenceLength}
							</div>
							<div>
								<b>Cosine Similarity:</b>
								{hit.score.toFixed(2)}
							</div>
							<div
								style="max-height: 100px; overflow-y: scroll; "
							>
								<b>Function:</b>
								{hit.function}
							</div>
						</div>
						<div></div>
					</div>
				</div>
			{/each}
		</div>
		<div class="flex justify-center m-5">
			{#if results && results.hits.length % 100 === 0}
				<Button
					color="alternative"
					on:click={async () => {
						topK += 100;
						await updateSearch(sequence, topK, selectedFilters);
					}}>Click to see more</Button
				>
			{/if}
		</div>
	{/if}
</main>

<style>
	.protein {
		outline: 1px solid rgba(255, 255, 255, 0.1);
		border-radius: 3px;
		width: 300px;
		padding: 15px;
	}
	.title {
		font-size: larger;
		font-weight: 500;
	}
</style>
